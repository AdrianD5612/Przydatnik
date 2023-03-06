from django.db import models, transaction
from django.utils import timezone
from django.contrib import admin
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('data opublikowania')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    @admin.display(     #wyświetlanie ostatnich ankiet dla admina
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text
    def save(self, *args, **kwargs):
        if not self.votes:
            return super(Choice, self).save(*args, **kwargs)
        with transaction.atomic():
            Choice.objects.filter(
                votes=True).update(votes=False)
            return super(Choice, self).save(*args, **kwargs)