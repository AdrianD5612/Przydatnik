from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index),
    path('theme', views.theme),
    path('add_note',views.add_note,name='add note'),
]