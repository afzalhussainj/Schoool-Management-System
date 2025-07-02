from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=200)
    isdeleted = models.BooleanField(default=False)

class SchoolBranch(models.Model):
    branch_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    isdeleted = models.BooleanField(default=False)