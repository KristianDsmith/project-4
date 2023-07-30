from django.contrib import admin
from .models import DietaryPreference, MenuItem, OperatingHours, Reservation, Table
from .models import Reservation



class DietaryPreferenceAdmin(admin.ModelAdmin):
    list_display = ['name']


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'dietary_preference']


class OperatingHoursAdmin(admin.ModelAdmin):
    list_display = ['day', 'opening_time', 'closing_time']


class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number']


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'table', 'date', 'time']


admin.site.register(DietaryPreference, DietaryPreferenceAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(OperatingHours, OperatingHoursAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Reservation)
