from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model that extends AbstractUser.
    Users can act as both buyers and sellers.
    The 'is_supervisor' field indicates if the user has administrative privileges.
    """
    is_supervisor = models.BooleanField(
        default=False,
        help_text="Indicates whether the user has supervisor privileges for administrative tasks."
    )

    def __str__(self):
        return self.username
