from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.utils import timezone
from utils.enumerations import RoleChoicesUsers
from utils.AutoFields import AutoFields

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
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user = self.create_user(email=email,password=password,**kwargs)
        user.role = RoleChoicesUsers.admin.value
        user.save()
        return user

class CustomUserModel(AbstractBaseUser, AutoFields):
    email = models.EmailField(blank=False, unique=True)
    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True
        )
    
    role = models.CharField(
        max_length=25,
        choices=[(e.value,e.name.title()) for e in RoleChoicesUsers]
        )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

