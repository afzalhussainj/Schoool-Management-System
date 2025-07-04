from django.db import models
from schools.models import SchoolBranch
from django.contrib.auth.models import AbstractUser,BaseUserManager

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

class CustomUserModel(AbstractUser):
    username = None
    email = models.EmailField(blank=False, unique=True)
    role_choices = (
        ('admin','Main Admin'),
        ('owner','School Owner'),
        ('manager','Branch Manager'),
        ('principal','Branch Principal'),
    )
    role = models.CharField(max_length=25,choices=role_choices)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    

# class Principal(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.EmailField(blank=False, unique=True)
#     password = models.CharField(max_length=50)
#     contact = models.CharField(max_length=25)
#     branch = models.OneToOneField(
#         SchoolBranch,
#         on_delete=models.PROTECT
#         )
#     branch = models.ForeignKey(
#         SchoolBranch,
#         on_delete=models.CASCADE,
#         related_name='principal'
#         )
#     isdeleted = models.BooleanField(default=False)

# class SchoolOwner(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.EmailField(blank=False, unique=True)
#     password = models.CharField(max_length=50)
#     contact = models.CharField(max_length=25)
#     school = models.ForeignKey(
#         SchoolBranch,
#         on_delete=models.CASCADE,
#         related_name='owner'
#         )
#     isdeleted = models.BooleanField(default=False)

# class BranchManager(models.Model):
    # name = models.CharField(max_length=20)
    # email = models.EmailField(blank=False, unique=True)
    # password = models.CharField(max_length=50)
    # contact = models.CharField(max_length=25)
    # branch = models.OneToOneField(
    #     SchoolBranch,
    #     on_delete=models.PROTECT,
    #     related_name='BranchManager'
    #     )
    # isdeleted = models.BooleanField(default=False)