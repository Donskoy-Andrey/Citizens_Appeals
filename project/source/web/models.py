from django.db import models
from django.utils import timezone


class Appeal(models.Model):

    text = models.TextField()
    sentiment = models.TextField(default="")
    executor = models.TextField()
    theme = models.TextField()
    group = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.text}: {self.theme} {self.date}"
