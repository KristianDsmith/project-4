from django.contrib import admin
from .models import MenuItem, DietaryPreference

admin.site.register(DietaryPreference)
admin.site.register(MenuItem)

