# Generated by Django 3.2.20 on 2023-09-04 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='is_set',
            field=models.BooleanField(default=False),
        ),
    ]