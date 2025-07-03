from django.db import models
from schools.models import SchoolBranch
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUserModel(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    role_choices = (
        ('admin','Main Admin'),
        ('owner','School Owner'),
        ('manager','Branch Manager'),
        ('principal','Branch Principal'),
    )
    role = models.CharField(max_length=25,choices=role_choices)

    USERNAME_FIELD = 'email'
    

class Principal(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=25)
    branch = models.OneToOneField(
        SchoolBranch,
        on_delete=models.PROTECT
        )
    branch = models.ForeignKey(
        SchoolBranch,
        on_delete=models.CASCADE,
        related_name='principal'
        )
    isdeleted = models.BooleanField(default=False)

class SchoolOwner(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=25)
    school = models.ForeignKey(
        SchoolBranch,
        on_delete=models.CASCADE,
        related_name='owner'
        )
    isdeleted = models.BooleanField(default=False)

class BranchManager(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=25)
    branch = models.OneToOneField(
        SchoolBranch,
        on_delete=models.PROTECT,
        related_name='BranchManager'
        )
    isdeleted = models.BooleanField(default=False)