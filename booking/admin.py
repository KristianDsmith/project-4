from django.contrib import admin
from .models import DietaryPreference, MenuItem, Rating, Booking

# Existing ModelAdmin classes


class DietaryPreferenceAdmin(admin.ModelAdmin):
    list_display = ['name']


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'dietary_preference']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_item', 'rating']

# Add a ModelAdmin for Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ['table', 'user', 'name', 'email',
                    'date', 'time', 'number_of_guests', 'canceled']
    # Optional: fields to filter by
    list_filter = ['date', 'canceled', 'table']
    # Assuming Table has a 'name' field
    search_fields = ['name', 'email', 'table__name']


# Register your models and their respective ModelAdmin
admin.site.register(DietaryPreference, DietaryPreferenceAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Booking, BookingAdmin)
