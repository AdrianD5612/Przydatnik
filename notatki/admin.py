from django.contrib import admin
from .models import *


class NotatkaAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'date_added', 'publicnote', 'author']
    list_display = ['title', 'content', 'date_added', 'publicnote', 'author']

admin.site.register(Notatka,NotatkaAdmin)