from django.db import models
from users.models import CustomUserModel
from utils.enumerations import RoleChoices

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=200)
    owner = models.OneToOneField(
        CustomUserModel,
        related_name='school',
        limit_choices_to={'role': RoleChoices.owner.value}
    )

class SchoolBranch(models.Model):
    branch_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='school_branch'
        )
    manager = models.OneToOneRel(
        CustomUserModel,
        limit_choices_to={'role':RoleChoices.manager.value},
        related_name='branch'
    )
    