from django.db import models


class Appeal(models.Model):

    text = models.TextField()
    executor = models.TextField()
    theme = models.TextField()
    group = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text}: {self.theme}"
