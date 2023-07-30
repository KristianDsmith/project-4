from django import forms


class BookingForm(forms.Form):
    date = forms.DateField()
    time = forms.TimeField()
