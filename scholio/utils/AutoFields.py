from django.db import models
from django.conf import settings
import uuid


class AutoFields(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
        )

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='updated_%(class)s',
        null=True,
        blank=True
        )
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_%(class)s',
        null=True,
        blank=True
        )

    class Meta:
        abstract = True

