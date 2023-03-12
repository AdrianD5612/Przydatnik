from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index),
    path('theme', views.theme),
    path('add_note',views.add_note,name='add note'),
    path('delete_note/<note_id>',views.delete_note,name='delete note'),
    path('edit_note/<note_id>',views.edit_note,name='edit note'),
    path('save_changes/<note_id>',views.save_changes, name='save changes'),
]