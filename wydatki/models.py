from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class AccountInfo(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    user_budget = models.IntegerField()
    
    def __str__(self):
        return self.username

class ExpenseInfo(models.Model):
    expense_name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    date_added = models.DateField()
    user_expense = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='images')

class Theme(models.Model):
    mode = models.CharField(max_length=10)
    user_theme = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_theme'], name='One Entry Per User')
        ]