from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        MEMBER = "member", "Member"
        LIBRARIAN = "librarian", "Librarian"
        
    role = models.CharField(
        max_length=20,choices=Role.choices, default=Role.MEMBER)
    
    def __str__(self):
        return self.username