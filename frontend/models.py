from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='frontend_user_groups',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='frontend_user_permissions',
        blank=True,
    )

    class Meta:
        permissions = [
            ("lgd_bd_access", "can access the lgd Models and update the location codes"),
            ("dataModel_access", "can update places"),
        ]