from django.db import models



class Table(models.Model):
    table_number = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_set = models.BooleanField(default=False) 

    def __str__(self):
        return f"Table {self.table_number}"


class ConfirmedDate(models.Model):
    date = models.DateField(unique=True)
    is_confirmed = models.BooleanField(default=False)
