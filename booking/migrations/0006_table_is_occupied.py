# Generated by Django 3.2.20 on 2023-08-02 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20230802_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='is_occupied',
            field=models.BooleanField(default=False),
        ),
    ]
