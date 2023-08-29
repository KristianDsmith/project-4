# Generated by Django 3.2.20 on 2023-08-27 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_delete_staffuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='title',
            field=models.CharField(default='Default Title', max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('PD', 'Pending'), ('CF', 'Confirmed'), ('CL', 'Cancelled')], default='PD', max_length=2),
        ),
    ]
