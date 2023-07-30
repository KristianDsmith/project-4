from django import forms
from .models import Table


class BookingForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    date = forms.DateField()
    time = forms.TimeField()
    table_number = forms.IntegerField()

    def clean_table_number(self):
        table_number = self.cleaned_data['table_number']
        try:
            table = Table.objects.get(table_number=table_number)
        except Table.DoesNotExist:
            raise forms.ValidationError(
                "Invalid table number. Please select a valid table.")
        return table_number
