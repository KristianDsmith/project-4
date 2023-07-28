from django.shortcuts import render
from .models import MenuItem, DietaryPreference
import cloudinary


def homepage(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def menu_view(request):
    try:
        menu_items = MenuItem.objects.all()
    except Exception as e:
        print(f"Error fetching menu items: {e}")
        menu_items = []

    return render(request, 'menu.html', {'menu_items': menu_items})


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

        # After processing the data, you may want to redirect the user to a confirmation page
        # For example, you can create a 'confirmation.html' template and render it here

        return render(request, 'confirmation.html', {'name': name, 'date': date, 'time': time})

    return render(request, 'book.html')


def contact(request):
    return render(request, 'contact.html')


def menu(request, dietary_preference_id=None):
    dietary_preferences = DietaryPreference.objects.all()
    selected_preference = None

    if dietary_preference_id is not None:
        selected_preference = DietaryPreference.objects.get(
            pk=dietary_preference_id)
        menu_items = MenuItem.objects.filter(
            dietary_preferences=selected_preference)
    else:
        menu_items = MenuItem.objects.all()

    context = {
        'menu_items': menu_items,
        'dietary_preferences': dietary_preferences,
        'selected_preference': selected_preference,
    }
    return render(request, 'menu.html', context)
