from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('bookingnumber', 'status')  

    def clean_bookingnumber(self):
        bookingnumber = self.cleaned_data.get('bookingnumber')
        if not bookingnumber:
            raise forms.ValidationError("Booking number is required.")
        return bookingnumber

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in ['1', '2', '3']:  
            raise forms.ValidationError("Invalid status.")
        return status
