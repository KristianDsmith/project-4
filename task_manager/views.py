from django.shortcuts import render, redirect
from task_manager.models import Table
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from booking.models import Booking  

@staff_member_required
def view_tasks(request):
    today = timezone.now().date()
    today_bookings = Booking.objects.filter(date=today)
    
    # Calculate the total number of guests
    total_guests = sum(booking.number_of_guests for booking in today_bookings)  
    
    # Calculate the total number of tables booked
    total_tables_booked = today_bookings.count()

    return render(request, 'view_tasks.html', {
        'total_guests': total_guests,
        'total_tables_booked': total_tables_booked,
    })
