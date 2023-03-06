from .models import ExpenseInfo  
from django import forms  
from django.forms import widgets
  
from django.db import models
from django.forms import ModelForm
  
class ExpenseDetails(forms.ModelForm):  #dodawanie nowego wydatku
    class Meta:
        model = ExpenseInfo
        fields = ('expense_name', 'cost',  'date_added' , 'image')
        labels = {
            'expense_name': 'Nazwa wydatku' , 'cost': 'Kwota', 'date_added': 'data', 'image':'obrazek',
        }
        widgets = {
            'date_added': widgets.DateInput(attrs={'type': 'date'})
        }
        