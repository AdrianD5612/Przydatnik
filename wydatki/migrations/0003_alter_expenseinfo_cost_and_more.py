# Generated by Django 4.1.5 on 2023-02-13 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wydatki', '0002_expenseinfo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseinfo',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='expenseinfo',
            name='expense_name',
            field=models.CharField(max_length=100),
        ),
    ]
