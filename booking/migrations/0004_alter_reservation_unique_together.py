# Generated by Django 3.2.20 on 2023-07-30 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_auto_20230730_1119'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('table', 'date', 'time')},
        ),
    ]
