from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    is_approved = models.BooleanField(default=False, help_text="Indicates whether the user is approved by an admin.")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
