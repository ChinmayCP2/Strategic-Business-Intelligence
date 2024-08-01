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
            ("lgd_access", "lgd data access"),
            ("data_model_access", "extracted data access"),
        ]