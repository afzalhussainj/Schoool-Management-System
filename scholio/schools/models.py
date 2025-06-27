from django.db import models
from ..users.models import SchoolOwner

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(SchoolOwner,on_delete=models.CASCADE,related_name='OwnedSchool')

class SchoolBranch(models.Model):
    branch_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    school = models.ForeignKey(School,on_delete=models.CASCADE)