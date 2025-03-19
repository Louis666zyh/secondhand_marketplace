from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    avatar = models.ImageField(upload_to="avatars/", default='img/no-image.png',null=True, blank=True)
    is_approved = models.BooleanField(default=False, help_text="Indicates whether the user is approved by an admin.")
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True, help_text="User's location.")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True)
    rating = models.FloatField(default=0.0)
    transactions = models.PositiveIntegerField(default=0, help_text="Number of completed transactions.")
    return_rate = models.FloatField(default=0.0, help_text="Return rate percentage.")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# apps.users.models.py
class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following',
        help_text="User who is following."
    )
    followee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers',
        help_text="User who is being followed."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the follow relationship was created.")

    class Meta:
        unique_together = ('follower', 'followee')  # 确保一个用户不能多次关注同一个用户

    def __str__(self):
        return f"{self.follower.username} follows {self.followee.username}"