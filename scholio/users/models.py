from django.db import models
from schools.models import SchoolBranch
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**kwargs):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email=email)
        user = self.model(email=email,**kwargs)
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
        user.role = 'admin'
        return user

class AutoUserFields(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='updated_%(class)s',
        null=True,
        blank=True
        )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='created_%(class)s',
        null=True,
        blank=True
        )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='deleted_%(class)s',
        null=True,
        blank=True
        )

    class Meta:
        abstract = True


class CustomUserModel(AbstractBaseUser, AutoUserFields):
    email = models.EmailField(blank=False, unique=True)
    role_choices = (
        ('admin','Main Admin'),
        ('owner','School Owner'),
        ('manager','Branch Manager'),
    )
    role = models.CharField(max_length=25,choices=role_choices)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

