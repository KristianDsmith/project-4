from django.shortcuts import render, redirect, get_object_or_404
from .models import Table, OperatingHours, Reservation
from .forms import BookingForm, ReservationUpdateForm
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import MenuItem, DietaryPreference
from django.conf import settings
from django_q.tasks import async_task
from .tasks import send_email_task
from django.views.generic import UpdateView
from django.urls import reverse_lazy


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
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    table=table,
                    date=date,
                    time=time,
                    number_of_guests=form.cleaned_data['number_of_guests'])
                reservation.save()

                subject = 'Table Booking Confirmation'
                message = f'Dear {reservation.name},\n\nThank you for booking a table. Your reservation details are as follows:\n\nTable Number: {reservation.table.table_number}\nDate: {reservation.date}\nTime: {reservation.time}\nNumber of Guests: {reservation.number_of_guests}\n\nWe look forward to seeing you!\n\nBest regards,\nThe Street Gastro Team'
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = reservation.email

                async_task(send_email_task, subject,
                           message, from_email, to_email)

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

        return response
