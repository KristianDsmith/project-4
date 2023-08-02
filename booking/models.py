from django.db import models
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

default_user_id = User.objects.first().id if User.objects.first() else None


class DietaryPreference(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')
    dietary_preference = models.ForeignKey(
        'DietaryPreference', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class OperatingHours(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day = models.CharField(choices=DAY_CHOICES, max_length=10)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return f"{self.get_day_display()}: {self.opening_time.strftime('%H:%M')} - {self.closing_time.strftime('%H:%M')}"


class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True)

    # New method to check table availability
    def is_available(self, date, time):
        reservations = Reservation.objects.filter(
            table=self, date=date, time=time)
        return not reservations.exists()

    def __str__(self):
        return f"Table {self.table_number}"


class Reservation(models.Model):
    name = models.CharField(max_length=100, default='Guest')
    email = models.EmailField(default='example@example.com')
    phone = models.CharField(max_length=15, default='N/A')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField(default=1)
    token = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)

    PENDING = 'PD'
    CONFIRMED = 'CF'
    CANCELLED = 'CL'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    def __str__(self):
        return f'{self.name} - {self.date} {self.time}'

    class Meta:
        unique_together = ['table', 'date', 'time']

    def __str__(self):
        return f"{self.name} - {self.table.table_number} - {self.date} - {self.time}"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class OnlineTableReservation(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    table = models.ForeignKey('Table', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.customer} reserved {self.table} on {self.date.strftime('%Y-%m-%d')} at {self.time.strftime('%H:%M')}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', default=default_user_id)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # This is the rating field

    def __str__(self):
        return f"{self.menu_item.name} - {self.rating} stars"

