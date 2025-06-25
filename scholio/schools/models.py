from django.db import models

# Create your models here.
class School(models.Model):
    branch_name = models.CharField(max_length=200)
    branch_address = models.CharField(max_length=1000)