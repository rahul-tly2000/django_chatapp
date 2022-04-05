from email import message
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatMessage(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message

