from .models import Notatka  
from django import forms  
from django.forms import widgets
  
from django.db import models
from django.forms import ModelForm
  
class NotatkaForm(forms.ModelForm):  #dodawanie nowej notatki
    
    class Meta:
        model = Notatka
        fields = ('title', 'publicnote',  'content')
        labels = {
            'title': 'Tytuł' , 'publicnote': 'Publiczna?', 'content':'Treść',
        }
        widgets = {
            'publicnote': forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'checkbox', 'id': 'your_id'})
        }