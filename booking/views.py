from django.shortcuts import render
from .models import MenuItem, DietaryPreference, OperatingHours, Table, Reservation


def homepage(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def book(request):
    if request.method == 'POST':
        # Process the form data when the user submits the booking form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        number_of_guests = request.POST.get('number_of_guests')

        # You can now perform any necessary actions with the form data
        # For example, saving the booking details to a database
        # Here, you can create a Reservation object

        reservation = Reservation.objects.create(
            table=Table.objects.get(pk=request.POST.get('table')),
            date=date,
            time=time,
        )

        # After processing the data, you may want to redirect the user to a confirmation page
        # For example, you can create a 'confirmation.html' template and render it here

        return render(request, 'confirmation.html', {'reservation': reservation})

    # Retrieve the operating hours for displaying on the book.html template
    operating_hours = OperatingHours.objects.all()

    # Retrieve all reservations to check the availability of tables
    all_reservations = Reservation.objects.all()

    context = {
        'operating_hours': operating_hours,
        'all_reservations': all_reservations,
    }

    return render(request, 'book.html', context)
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


def restaurant_hours(request):
    hours = OperatingHours.objects.all()
    return render(request, 'book.html', {'hours': hours})
