from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django_q.tasks import async_task
from django.db.models import Avg
from .models import MenuItem, DietaryPreference, Rating, Booking
from django.views.generic.edit import CreateView
import json
from booking.models import Booking
from .forms import BookingForm 







def homepage(request):
    # Fetch bookings or create a new booking as needed
    bookings = Booking.objects.all()  # Fetch all bookings or apply appropriate filters
    
    context = {
        'bookings': bookings,  # Pass the bookings to the template
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')

def book(request):
    return render(request, 'book.html')


def contact(request):
    return render(request, 'contact.html')


def menu_view(request):
    dietary_preference_id = request.GET.get('dietary_preference_id', None)

    menu_items = MenuItem.objects.all()
    if dietary_preference_id:
        menu_items = menu_items.filter(dietary_preference_id=dietary_preference_id)

    dietary_preferences = DietaryPreference.objects.all()
    
    for item in menu_items:
        ratings = Rating.objects.filter(menu_item=item)  # assumes you have a Rating model
        average_rating = ratings.aggregate(Avg('rating'))['rating__avg']  # Use 'rating' instead of 'value'
        item.average_rating = average_rating if average_rating is not None else 0

    context = {
        'menu_items': menu_items,
        'dietary_preferences': dietary_preferences,
        'selected_preference': dietary_preference_id,
    }

    return render(request, 'menu.html', context)


def submit_rating(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        menu_item_id = data.get('menu_item_id')
        rating_value = data.get('rating')

        try:
            menu_item = MenuItem.objects.get(pk=menu_item_id)
            new_rating = Rating.objects.create(menu_item=menu_item, rating=rating_value)
            new_average_rating = menu_item.ratings.all().aggregate(Avg('rating'))['rating__avg']  # Assuming 'ratings' is the related_name for ratings in the MenuItem model

            print(f"New average rating for menu item {menu_item_id}: {new_average_rating}")  # Add this line

            return JsonResponse({"average_rating": new_average_rating}, status=200)
        except MenuItem.DoesNotExist:
            return JsonResponse({"error": "Menu item not found."}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=400)


def menu_item_detail(request, menu_item_id):
    try:
        menu_item = MenuItem.objects.get(pk=menu_item_id)
    except MenuItem.DoesNotExist:
        return HttpResponse("Menu item not found.", status=404)

    context = {
        'menu_item': menu_item,
    }
    return render(request, 'menu_item_detail.html', context)


def book(request):
    if request.method == 'POST':
        print(request.POST)  # Print the submitted data to the console for debugging
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        number_of_guests = request.POST.get('number_of_guests')
        
        booking = Booking.objects.create(
            name=name,
            email=email,
            date=date,
            time=time,
            number_of_guests=number_of_guests
        )
        return render(request, 'thank_you.html')
    
    return render(request, 'index.html')

from django.contrib import messages
from django.shortcuts import render
from .models import Booking

def edit_booking(request, booking_id=None):
    bookings = None
    selected_booking = None

    if request.method == 'POST':
        if 'search_email' in request.POST:
            email = request.POST.get('email')
            bookings = Booking.objects.filter(email=email)
            
            if not bookings.exists():
                messages.error(request, "No bookings found for this email")
                return render(request, 'edit_booking.html', {'bookings': None})
        
        elif 'select_booking' in request.POST:
            selected_booking_id = request.POST.get('selected_booking_id')
            selected_booking = Booking.objects.get(id=selected_booking_id)
        
        elif 'edit_booking' in request.POST:
            selected_booking_id = request.POST.get('booking_id')
            selected_booking = Booking.objects.get(id=selected_booking_id)
            
            # Getting and validating the updated data
            name = request.POST.get('name')
            email = request.POST.get('email')
            date = request.POST.get('date')
            time = request.POST.get('time')
            
            # Placeholder for validation; implement your own logic
            if not name or not email or not date or not time:
                messages.error(request, 'All fields are required.')
                return render(request, 'edit_booking.html', {'selected_booking': selected_booking})
            
            # Updating and saving the object
            selected_booking.name = name
            selected_booking.email = email
            selected_booking.date = date
            selected_booking.time = time
            selected_booking.save()
            
            # Confirm and redirect
            messages.success(request, 'Booking updated successfully.')
            return redirect('edit_confirmation', booking_id=selected_booking_id)

    return render(request, 'edit_booking.html', {'bookings': bookings, 'selected_booking': selected_booking})






def cancel_booking(request, booking_id=None):
    email = None
    bookings = None
    booking = None

    if 'search_email' in request.POST:
        email = request.POST.get('email', '')
        bookings = Booking.objects.filter(email=email)
        
        if not bookings.exists():
            messages.error(request, 'No bookings found for this email.')
        elif bookings.count() == 1:
            booking = bookings.first()

    elif 'confirm_cancel' in request.POST:
        booking_id = request.POST.get('booking_id', '')
        booking = Booking.objects.get(id=booking_id)
        booking.delete()  # Assuming you want to delete the booking, change if needed
        
        messages.success(request, 'Your booking has been successfully canceled.')
        
        return redirect('cancellation_confirmation')  # Redirecting to the new confirmation page

    return render(request, 'cancel_booking.html', {'bookings': bookings, 'booking': booking})


def confirm_cancel(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return redirect('some-error-page-or-404')

    if request.method == 'POST':
        booking.canceled = True
        booking.save()
        messages.success(request, 'Your booking has been successfully canceled.')
        return redirect('homepage')
        
    return render(request, 'confirm_cancel.html', {'booking': booking})


def cancellation_confirmation(request):
    return render(request, 'cancellation_confirmation.html')

def edit_confirmation(request, booking_id):
    return render(request, 'edit_confirmation.html', {'booking_id': booking_id})































