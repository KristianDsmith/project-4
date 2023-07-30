from django.shortcuts import render, redirect
from .models import Table, OperatingHours, Reservation
from .forms import BookingForm
from django.contrib import messages
from .models import MenuItem
from .models import DietaryPreference




def homepage(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def restaurant_hours(request):
    hours = OperatingHours.objects.all()
    return render(request, 'restaurant_hours.html', {'hours': hours})


def book(request):
    operating_hours = OperatingHours.objects.all()
    tables = Table.objects.all()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            table_number = form.cleaned_data['table_number']
            table = Table.objects.get(table_number=table_number)

            if table.is_available(date, time):
                reservation = Reservation(name=form.cleaned_data['name'],
                                          email=form.cleaned_data['email'],
                                          phone=form.cleaned_data['phone'],
                                          table=table,
                                          date=date,
                                          time=time)
                reservation.save()
                messages.success(request, 'Table booked successfully!')
                return redirect('book')
            else:
                messages.error(
                    request, 'Table is already booked for the selected date and time.')
        else:
            messages.error(
                request, 'Invalid form submission. Please check the form data.')

    else:
        form = BookingForm()

    return render(request, 'book.html', {'form': form, 'tables': tables, 'operating_hours': operating_hours})


def book_table(request):
    tables = Table.objects.all()
    operating_hours = OperatingHours.objects.all()

    # Get all reserved tables for the selected date and time
    reserved_tables = Reservation.objects.filter(date=request.POST.get(
        'date'), time=request.POST.get('time')).values_list('table', flat=True)

    available_tables = [
        table for table in tables if table.id not in reserved_tables]

    return render(request, 'book.html', {'tables': available_tables, 'operating_hours': operating_hours})


def contact(request):
    return render(request, 'contact.html')


def menu_view(request):
    dietary_preference_id = request.GET.get('dietary_preference_id')

    if dietary_preference_id:
        try:
            selected_preference = DietaryPreference.objects.get(
                pk=dietary_preference_id)
            menu_items = MenuItem.objects.filter(
                dietary_preference=selected_preference)
        except DietaryPreference.DoesNotExist:
            menu_items = MenuItem.objects.all()
    else:
        menu_items = MenuItem.objects.all()

    dietary_preferences = DietaryPreference.objects.all()

    context = {
        'menu_items': menu_items,
        'dietary_preferences': dietary_preferences,
        'selected_preference': dietary_preference_id,
    }

    return render(request, 'menu.html', context)
