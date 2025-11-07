from django import forms
from .models import Airport, Passenger, Flight

class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ['code', 'name']

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'email', 'phone']

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['passenger', 'departure_airport', 'arrival_airport', 'date_time']