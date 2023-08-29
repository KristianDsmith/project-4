from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

# STATUS_CHOICES
PENDING = 'PD'
CONFIRMED = 'CF'
CANCELLED = 'CL'
STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (CONFIRMED, 'Confirmed'),
    (CANCELLED, 'Cancelled'),
]

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
        DietaryPreference, on_delete=models.SET_NULL, null=True)

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
    is_occupied = models.BooleanField(default=False)

    def is_available(self, date):
        reservations = Reservation.objects.filter(table=self, date=date)
        return not reservations.exists()

    def toggle_occupied(self):
        self.is_occupied = not self.is_occupied
        self.save()

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
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)

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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.customer} reserved {self.table} on {self.date.strftime('%Y-%m-%d')} at {self.time.strftime('%H:%M')}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.menu_item.name} - {self.rating} stars"

class Task(models.Model):
    title = models.CharField(max_length=200, default="Default Title")
    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='assigned_tasks')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='confirmed_tasks')
    staff_or_manager = models.CharField(max_length=10, choices=[('staff', 'Staff'), ('manager', 'Manager')], default='staff')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

