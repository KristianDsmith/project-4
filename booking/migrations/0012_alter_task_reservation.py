# Generated by Django 3.2.20 on 2023-08-27 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_auto_20230827_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.reservation'),
        ),
    ]
