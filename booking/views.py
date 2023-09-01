from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django_q.tasks import async_task
from .models import MenuItem, DietaryPreference, Rating
from django.views.generic import UpdateView
from django.db.models import Avg
import json
from .models import Booking
from .forms import BookingForm
from django.contrib import messages




def homepage(request):
    return render(request, 'index.html')


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
