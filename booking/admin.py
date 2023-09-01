from django.contrib import admin
from .models import DietaryPreference, MenuItem, Rating

# Make sure all these models exist in your models.py

class DietaryPreferenceAdmin(admin.ModelAdmin):
    list_display = ['name']

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'dietary_preference']

class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_item', 'rating']

admin.site.register(DietaryPreference, DietaryPreferenceAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Rating, RatingAdmin)
