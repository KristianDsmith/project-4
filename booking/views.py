import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django_q.tasks import async_task
from .models import Table, OperatingHours, Reservation, MenuItem, DietaryPreference, Rating
from .forms import BookingForm, ReservationUpdateForm, RatingForm
from .tasks import send_email_task
from django.views.generic import UpdateView
from django.db.models import Avg
from django.http import JsonResponse


# Helper function to send email
def send_email(subject, message, from_email, to_email):
    try:
        async_task(send_email_task, subject, message, from_email, to_email)
    except Exception as e:
        print(f"Error sending email: {e}")


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
    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            reservation = form.save()

            update_url = request.build_absolute_uri(
                reverse('update_reservation', args=[reservation.id]))

            subject = 'Table Booking Confirmation'
            message = f'Dear {reservation.name},\n\nThank you for booking a table. Your reservation details are as follows:\n\nTable Number: {reservation.table.table_number}\nDate: {reservation.date}\nTime: {reservation.time}\nNumber of Guests: {reservation.number_of_guests}\n\nTo make any changes to your reservation, please click on the following link:\n{update_url}\n\nWe look forward to seeing you!\n\nBest regards,\nThe Street Gastro Team'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = reservation.email

            send_email(subject, message, from_email, to_email)
            
            messages.success(request, 'Table booked successfully! A confirmation email has been sent to your email address.')
            return redirect('book')
        else:
            messages.error(request, 'Invalid form submission. Please check the form data.')
    return render(request, 'book.html', {'form': form, 'tables': tables, 'operating_hours': operating_hours})


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



class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationUpdateForm
    template_name = 'update_reservation.html'
    success_url = reverse_lazy('book')

    def form_valid(self, form):
        response = super().form_valid(form)
        reservation = self.object

        if reservation.status == Reservation.CANCELLED:
            subject = 'Table Reservation Cancelled'
            message = f'Dear {reservation.name},\n\nYour reservation has been cancelled as per your request.\n\nBest regards,\nThe Street Gastro Team'
        else:
            subject = 'Table Reservation Modified'
            message = f'Dear {reservation.name},\n\nYour reservation has been modified. Your new reservation details are as follows:\n\nTable Number: {reservation.table.table_number}\nDate: {reservation.date}\nTime: {reservation.time}\nNumber of Guests: {reservation.number_of_guests}\n\nWe look forward to seeing you!\n\nBest regards,\nThe Street Gastro Team'

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = reservation.email

        send_email(subject, message, from_email, to_email)

        messages.success(self.request, 'Reservation updated successfully!')
        return response


def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == 'POST':
        reservation.status = Reservation.CANCELLED
        reservation.save()  # Save the changes to the database

        # Send cancellation confirmation email (optional)
        subject = 'Table Reservation Cancelled'
        message = f'Dear {reservation.name},\n\nYour reservation has been cancelled as per your request.\n\nBest regards,\nThe Street Gastro Team'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = reservation.email

        send_email(subject, message, from_email, to_email)

        messages.success(request, 'Reservation has been cancelled successfully!')
        return redirect('book')

    return render(request, 'cancel_reservation.html', {'reservation': reservation})


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
