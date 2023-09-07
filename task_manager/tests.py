from django.test import TestCase
from datetime import datetime, date
from .models import Table, ConfirmedDate  
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from booking.models import Booking
from task_manager.models import Table
from .models import ConfirmedDate


class TableTestCase(TestCase):
    def setUp(self):
        Table.objects.create(table_number=1, is_available=True, is_set=False)
        Table.objects.create(table_number=2, is_available=False, is_set=True)

    def test_table_str(self):
        table1 = Table.objects.get(table_number=1)
        table2 = Table.objects.get(table_number=2)
        self.assertEqual(str(table1), "Table 1")
        self.assertEqual(str(table2), "Table 2")

    def test_table_availability(self):
        table1 = Table.objects.get(table_number=1)
        self.assertEqual(table1.is_available, True)

class ConfirmedDateTestCase(TestCase):
    def setUp(self):
        ConfirmedDate.objects.create(date=date.today(), is_confirmed=True)

    def test_date_str(self):
        confirmed_date = ConfirmedDate.objects.get(date=date.today())
        self.assertEqual(str(confirmed_date.date), str(date.today()))

    def test_date_confirmation(self):
        confirmed_date = ConfirmedDate.objects.get(date=date.today())
        self.assertEqual(confirmed_date.is_confirmed, True)

