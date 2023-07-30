from django.db import models
from booking.models.table import Table


class Reservation(models.Model):
    name = models.CharField(max_length=100, default='Guest')
    email = models.EmailField(default='example@example.com')
    phone = models.CharField(max_length=15, default='N/A')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        unique_together = ['table', 'date', 'time']

    def __str__(self):
        return f"{self.name} - {self.table.table_number} - {self.date} - {self.time}"
