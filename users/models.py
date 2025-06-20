from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        MANAGER = 'Manager', 'Manager'
        USER = 'User', 'User'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)

    def __str__(self):
        return f"{self.username} ({self.role})"
