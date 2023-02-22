# Generated by Django 4.1.5 on 2023-02-22 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wydatki', '0003_alter_expenseinfo_cost_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(max_length=10)),
                ('user_theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='theme',
            constraint=models.UniqueConstraint(fields=('user_theme',), name='One Entry Per User'),
        ),
    ]
