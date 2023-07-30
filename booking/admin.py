from django.contrib import admin
from .models import DietaryPreference, MenuItem, OperatingHours, Table, Reservation, Customer, OnlineTableReservation

admin.site.register(DietaryPreference)
admin.site.register(MenuItem)
admin.site.register(OperatingHours)
admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Customer)
admin.site.register(OnlineTableReservation)
