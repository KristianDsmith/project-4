from django.contrib import admin
from .models import Table, OperatingHours, Reservation, MenuItem, DietaryPreference
from .models import Rating



class DietaryPreferenceAdmin(admin.ModelAdmin):
    list_display = ['name']


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'dietary_preference']


class OperatingHoursAdmin(admin.ModelAdmin):
    list_display = ['day', 'opening_time', 'closing_time']


class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number']


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone',
                    'table', 'date', 'time', 'number_of_guests', 'update_link']

    def update_link(self, obj):
        url = reverse("update_reservation", args=[obj.id])
        return format_html('<a href="{}">Update</a>', url)

    update_link.short_description = 'Update Reservation'

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'table', 'date', 'time', 'number_of_guests', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'email', 'phone', 'table__table_number')

class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_item', 'rating'] 


admin.site.register(DietaryPreference, DietaryPreferenceAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(OperatingHours, OperatingHoursAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Rating, RatingAdmin)
