from django import forms
from .models import Table
from .models import Reservation, Rating


class BookingForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    date = forms.DateField()
    time = forms.TimeField()
    table_number = forms.IntegerField()
    number_of_guests = forms.IntegerField()

    def clean_table_number(self):
        table_number = self.cleaned_data['table_number']
        try:
            table = Table.objects.get(table_number=table_number)
        except Table.DoesNotExist:
            raise forms.ValidationError(
                "Invalid table number. Please select a valid table.")
        return table_number


class ReservationUpdateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'table',
                  'date', 'time', 'number_of_guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']


class ConfirmBookingForm(forms.Form):
    confirm = forms.BooleanField(label='Confirm Booking')