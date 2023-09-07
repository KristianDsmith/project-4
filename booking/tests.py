from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import DietaryPreference, MenuItem, Rating, Booking
from django.contrib.auth.models import User
from unittest.mock import patch
from .models import Booking
from .models import MenuItem, DietaryPreference



class DietaryPreferenceTestCase(TestCase):

    def setUp(self):
        DietaryPreference.objects.create(name="Vegetarian")

    def test_str_representation(self):
        preference = DietaryPreference.objects.get(name="Vegetarian")
        self.assertEqual(str(preference), "Vegetarian")


class MenuItemTestCase(TestCase):

    def setUp(self):
        DietaryPreference.objects.create(name="Vegan")
        preference = DietaryPreference.objects.get(name="Vegan")
        MenuItem.objects.create(
            name="Salad", description="Green Salad", price="9.99", dietary_preference=preference)

    def test_str_representation(self):
        item = MenuItem.objects.get(name="Salad")
        self.assertEqual(str(item), "Salad")


class RatingTestCase(TestCase):

    def setUp(self):
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user = User.objects.get(username='john')
        MenuItem.objects.create(name="Burger", description="Cheese Burger", price="12.99")
        item = MenuItem.objects.get(name="Burger")
        Rating.objects.create(user=user, menu_item=item, rating=4)

    def test_str_representation(self):
        rating = Rating.objects.get(rating=4)
        self.assertEqual(str(rating), "Burger - 4 stars")


class BookingTestCase(TestCase):

    def setUp(self):
        User.objects.create_user('paul', 'mccartney@thebeatles.com', 'paulpassword')
        user = User.objects.get(username='paul')
        Booking.objects.create(user=user, name="Paul", email="paul@test.com", date="2023-09-01", time="12:00", number_of_guests=2)

    def __str__(self):
        formatted_time = self.time.strftime('%H:%M')  
        return f'{self.name} - {self.date} - {formatted_time}'



