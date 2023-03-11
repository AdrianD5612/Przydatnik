from django.db import models
from django.contrib.auth.models import User


class Notatka(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    date_added = models.DateField()
    publicnote = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)