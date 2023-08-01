import uuid
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
from .forms import RatingForm

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
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            table_number = form.cleaned_data['table_number']
            number_of_guests = form.cleaned_data['number_of_guests']

            try:
                table = Table.objects.get(table_number=table_number)
            except Table.DoesNotExist:
                messages.error(
                    request, "Invalid table number. Please select a valid table.")
                return redirect('book')

            if table.is_available(date, time):
                reservation = Reservation(
                    name=name,
                    email=email,
                    phone=phone,
                    table=table,
                    date=date,
                    time=time,
                    number_of_guests=number_of_guests)
                reservation.save()

                # Generate the unique link
                update_link = generate_booking_update_link(reservation.id)
                if update_link:
                    # Construct the URL for the update_reservation view
                    update_url = request.build_absolute_uri(
                        reverse('update_reservation', args=[update_link]))

                    # Send the confirmation email with the update URL
                    subject = 'Table Booking Confirmation'
                    message = f'Dear {reservation.name},\n\nThank you for booking a table. Your reservation details are as follows:\n\nTable Number: {reservation.table.table_number}\nDate: {reservation.date}\nTime: {reservation.time}\nNumber of Guests: {reservation.number_of_guests}\n\nTo make any changes to your reservation, please click on the following link:\n{update_url}\n\nWe look forward to seeing you!\n\nBest regards,\nThe Street Gastro Team'
                    from_email = settings.DEFAULT_FROM_EMAIL
                    to_email = reservation.email

                    async_task(send_email_task, subject, message, from_email, to_email)

                    messages.success(
                        request, 'Table booked successfully! A confirmation email has been sent to your email address.')
                    return redirect('book')
                else:
                    messages.error(
                        request, 'Failed to generate update link.')
            else:
                messages.error(
                    request, 'Table is already booked for the selected date and time.')
        else:
            messages.error(
                request, 'Invalid form submission. Please check the form data.')
    else:
        form = BookingForm()

    # Handle Reservation Cancellation
    if request.method == 'GET' and 'cancel_reservation' in request.GET:
        token = request.GET['cancel_reservation']
        reservation = get_object_or_404(Reservation, token=token)

        if reservation.status == Reservation.PENDING:
            reservation.delete()
            messages.success(request, 'Reservation successfully cancelled.')
        else:
            messages.error(
                request, 'Cannot cancel reservation. Reservation is already confirmed.')

    return render(request, 'book.html', {'form': form, 'tables': tables, 'operating_hours': operating_hours})


def contact(request):
    return render(request, 'contact.html')


def menu_view(request):
    dietary_preference_id = request.GET.get('dietary_preference_id')

    if dietary_preference_id:
        try:
            selected_preference = DietaryPreference.objects.get(pk=dietary_preference_id)
            menu_items = MenuItem.objects.filter(dietary_preference=selected_preference)
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


def confirm_reservation(request):
    # Your code to confirm the reservation and send confirmation email
    return HttpResponse('Reservation confirmed. Confirmation email sent.')


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

        async_task(send_email_task, subject, message, from_email, to_email)

        messages.success(self.request, 'Reservation updated successfully!')
        return response


def generate_booking_update_link(booking_id):
    try:
        booking = Reservation.objects.get(id=booking_id)
        return booking.pk
    except Reservation.DoesNotExist:
        return None


def cancel_reservation(request, token):
    reservation = get_object_or_404(Reservation, token=token)

    if request.method == 'POST':
        reservation.status = Reservation.CANCELLED
        reservation.save()  # Save the changes to the database

        # Send cancellation confirmation email (optional)
        subject = 'Table Reservation Cancelled'
        message = f'Dear {reservation.name},\n\nYour reservation has been cancelled as per your request.\n\nBest regards,\nThe Street Gastro Team'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = reservation.email

        async_task(send_email_task, subject, message, from_email, to_email)

        messages.success(request, 'Reservation has been cancelled successfully!')
        return redirect('book')

    return render(request, 'cancel_reservation.html', {'reservation': reservation})


from django.http import JsonResponse
from django.db.models import Avg

def menu(request):
    if request.method == 'POST' and request.is_ajax():
        menu_item_id = request.POST.get('menu_item_id')
        rating = int(request.POST.get('rating'))

        # Save the rating to the database (you can use the Rating model)
        # Replace the following lines with your actual code to save the rating
        # rating_obj = Rating.objects.create(menu_item_id=menu_item_id, rating=rating)
        # average_rating = rating_obj.menu_item.ratings.aggregate(models.Avg('rating'))['rating__avg']

        # For demonstration purposes, return the average rating as a JSON response
        # You should replace this with the actual average_rating value
        average_rating = 4.2
        response_data = {
            'average_rating': average_rating
        }

        return JsonResponse(response_data)

    # If the request is not a POST or not AJAX, return a 404 error
    return JsonResponse({'error': 'Invalid request.'}, status=404)





def menu_item_detail(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    ratings = Rating.objects.filter(menu_item=menu_item)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            Rating.objects.create(menu_item=menu_item, rating=rating)
            return redirect('menu_item_detail', menu_item_id=menu_item_id)
    else:
        form = RatingForm()

    return render(request, 'menu_item_detail.html', {'menu_item': menu_item, 'form': form, 'ratings': ratings, 'average_rating': average_rating})