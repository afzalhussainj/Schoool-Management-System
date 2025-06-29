from django.db import models
from schools.models import SchoolBranch

# Create your models here.
class Principal(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=25)
    branch = models.OneToOneField(SchoolBranch, on_delete=models.PROTECT)
    branch = models.ForeignKey(SchoolBranch, on_delete=models.CASCADE, related_name='principal')

class SchoolOwner(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=25)
    school = models.ForeignKey(SchoolBranch,on_delete=models.CASCADE,related_name='owner')
    
class BranchManager(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=25)
    branch = models.OneToOneField(SchoolBranch, on_delete=models.PROTECT, related_name='BranchManager')
