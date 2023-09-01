# Generated by Django 3.2.20 on 2023-09-01 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0015_alter_reservation_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onlinetablereservation',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='onlinetablereservation',
            name='table',
        ),
        migrations.DeleteModel(
            name='OperatingHours',
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='table',
        ),
        migrations.RemoveField(
            model_name='task',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='task',
            name='confirmed_by',
        ),
        migrations.RemoveField(
            model_name='task',
            name='reservation',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='OnlineTableReservation',
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
        migrations.DeleteModel(
            name='Table',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
