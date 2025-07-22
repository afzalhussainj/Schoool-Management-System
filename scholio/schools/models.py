from django.db import models
from users.models import CustomUserModel
from utils.enumerations import RoleChoicesUsers

class School(models.Model):
    name = models.CharField(max_length=200)
    owner = models.OneToOneField(
        CustomUserModel,
        related_name='school',
        limit_choices_to={'role': RoleChoicesUsers.owner.value},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class SchoolBranch(models.Model):
    branch_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='school_branch',
        null=True,
        blank=True
        )
    manager = models.OneToOneField(
        CustomUserModel,
        limit_choices_to={'role':RoleChoicesUsers.manager.value},
        related_name='branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    