from django.db import models
from django.apps import apps
from apps.users.models import User
from apps.products.models import Product

class Message(models.Model):
    """
    Model representing a direct message between users.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages',
                               help_text="User sending the message.")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages',
                                 help_text="User receiving the message.")
    content = models.TextField(help_text="Content of the message.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the message was sent.")

    class Meta:
        app_label = 'chat'

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"