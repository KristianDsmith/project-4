from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Table, OperatingHours, Reservation, MenuItem, DietaryPreference, Rating, Task

# STATUS_CHOICES
PENDING = 'PD'
CONFIRMED = 'CF'
CANCELLED = 'CL'
STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (CONFIRMED, 'Confirmed'),
    (CANCELLED, 'Cancelled'),
]

class DietaryPreferenceAdmin(admin.ModelAdmin):
    list_display = ['name']

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'dietary_preference']

class OperatingHoursAdmin(admin.ModelAdmin):
    list_display = ['day', 'opening_time', 'closing_time']

class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number']

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'table', 'date', 'time', 'number_of_guests', 'status', 'update_link')
    list_filter = ('date', 'status',)
    search_fields = ('name', 'email', 'phone', 'table__table_number',)
    ordering = ('-date', '-time',)
    readonly_fields = ('token',)

    def update_link(self, obj):
        url = reverse("update_reservation", args=[obj.id])
        return format_html('<a href="{}">Update</a>', url)

    update_link.short_description = 'Update Reservation'

class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_item', 'rating']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'due_date', 'completed', 'reservation', 'assigned_to', 'staff_or_manager', 'status']
    search_fields = ['title']
    list_filter = ['status', 'staff_or_manager', 'completed']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs.filter(assigned_to=request.user)
        return qs

admin.site.register(DietaryPreference, DietaryPreferenceAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(OperatingHours, OperatingHoursAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Task, TaskAdmin)
