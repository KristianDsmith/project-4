from django import forms
from .models import Rating
from .models import Booking


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']

class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'text'}))
    time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'text'}))

    class Meta:
        model = Booking
        fields = ['name', 'email', 'date', 'time', 'number_of_guests']
