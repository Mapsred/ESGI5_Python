from django.db import models

from accounts.models import Profile


class Message(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipient')
    date_sent = models.IntegerField()
    text = models.TextField()
    read = models.BooleanField(default=False)
