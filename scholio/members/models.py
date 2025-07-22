from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
import uuid
from django.utils import timezone
from utils.enumerations import RoleChoicesMembers
from utils.AutoFields import AutoFields

# Create your models here.

class CustomMemberManager(BaseUserManager):
    def create_user(self,email,password,**kwargs):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email=email)
        Member = self.model(email=email,**kwargs)
        Member.created_by = kwargs.get('created_by')
        Member.set_password(password)
        Member.save()
        return Member


class GuardianModel(AbstractBaseUser, AutoFields):
    number = models.CharField(blank=False, unique=True)
    email = models.EmailField(blank=True,null=True)
    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True
        )

    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = []

    objects = CustomMemberManager()


class StudentModel(AbstractBaseUser, AutoFields):
    username = models.CharField(unique=True)
    f_name = models.CharField(max_length=10)
    l_name = models.CharField(max_length=10)
    email = models.EmailField(blank=True,null=True)
    number = models.CharField(blank=True,null=True)
    address = models.CharField(max_length=250)
    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True
        )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def create_user(self,password,**kwargs):
        Member = self.model(**kwargs)
        Member.username = str(self.f_name) + (str(self.uuid)[:3] + str(self.uuid)[-3:])
        Member.created_by = kwargs.get('created_by')
        Member.set_password(password)
        Member.save()
        return Member

