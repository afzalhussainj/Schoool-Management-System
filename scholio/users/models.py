from django.db import models
from schools.models import School

# Create your models here.
class Principal(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=25)
    branch = models.ForeignKey(School, on_delete=models.CASCADE, related_name='principal')