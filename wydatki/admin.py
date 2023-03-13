from django.contrib import admin

from .models import *


class ExpenseInfoAdmin(admin.ModelAdmin):
    fields = ['expense_name', 'cost', 'date_added', 'user_expense', 'image']
    list_display = ['expense_name', 'cost', 'date_added', 'user_expense']

class ThemeAdmin(admin.ModelAdmin):
    fields = ['ser_theme','mode']
    list_display = ['user_theme','mode']

admin.site.register(ExpenseInfo, ExpenseInfoAdmin)
admin.site.register(Theme, ThemeAdmin)