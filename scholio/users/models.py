from django.db import models
from schools.models import SchoolBranch
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
import uuid
from django.utils import timezone
from utils.enumerations import RoleChoices

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**kwargs):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email=email)
        user = self.model(email=email,**kwargs)
        user.created_by = kwargs.get('created_by')
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user = self.create_user(email=email,password=password,**kwargs)
        user.role = RoleChoices.admin.value
        user.save()
        return user

class AutoUserFields(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
        )

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='updated_%(class)s',
        null=True,
        blank=True
        )
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_%(class)s',
        null=True,
        blank=True
        )
    
    deleted_at = models.DateTimeField(blank=True,null=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='deleted_%(class)s',
        null=True,
        blank=True
        )

    class Meta:
        abstract = True


class CustomUserModel(AbstractBaseUser, AutoUserFields):
    email = models.EmailField(blank=False, unique=True)
    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True
        )
    
    role = models.CharField(
        max_length=25,
        choices=[(e.value,e.name.title()) for e in RoleChoices]
        )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def delete(self,user):
        self.is_active = False
        self.deleted_by = user
        self.deleted_at = timezone.now()
        self.save()

    def update(self,**kwargs):
        return ''

