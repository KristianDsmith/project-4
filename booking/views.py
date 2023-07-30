from django.shortcuts import render
from .models import MenuItem, DietaryPreference, OperatingHours, Table, Reservation


def homepage(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def restaurant_hours(request):
    hours = OperatingHours.objects.all()
    return render(request, 'restaurant_hours.html', {'hours': hours})


def book(request):
    operating_hours = OperatingHours.objects.all()

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Get all tables
        tables = Table.objects.all()

        # Filter tables that are not reserved on the selected date and time
        available_tables = []
        for table in tables:
            if not Reservation.objects.filter(table=table, date=date, time=time).exists():
                available_tables.append(table)

        return render(request, 'book.html', {'tables': available_tables, 'operating_hours': operating_hours})

    # If it's a GET request or the form is not submitted, render the empty form
    return render(request, 'book.html', {'operating_hours': operating_hours})


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
