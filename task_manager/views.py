from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from booking.models import Booking
from task_manager.models import Table
from datetime import timedelta, datetime
from django.contrib import messages
from .models import ConfirmedDate 
from django.http import HttpResponse  


@staff_member_required
def view_tasks(request):
    today = timezone.now().date()
    weekdays = [(today + timedelta(days=i)) for i in range(7)]
    confirmed_dates = list(ConfirmedDate.objects.filter(is_confirmed=True).values_list('date', flat=True))

    selected_date = request.GET.get('selected_date')
    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            bookings_on_selected_date = Booking.objects.filter(date=selected_date)
            total_guests = sum(booking.number_of_guests for booking in bookings_on_selected_date)
            total_tables_booked = bookings_on_selected_date.count()
            tables = Table.objects.all()

            return render(request, 'view_task_details.html', {
                'selected_date': selected_date,
                'total_guests': total_guests,
                'total_tables_booked': total_tables_booked,
                'tables': tables,
                'confirmed_dates': confirmed_dates,
            })

        except ValueError:
            return HttpResponse("Incorrect date format. Expected 'YYYY-MM-DD'.")

    return render(request, 'view_tasks.html', {
        'weekdays': weekdays,
        'confirmed_dates': confirmed_dates,
    })
