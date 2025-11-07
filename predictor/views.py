from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from collections import Counter
import random
from .models import Airport, Passenger, Flight, Prediction
from .forms import AirportForm, PassengerForm, FlightForm
from collections import Counter

def home(request):
    passengers = Passenger.objects.filter(is_archived=False)
    return render(request, 'predictor/home.html', {'passengers': passengers})

def select_passenger_for_predictions(request):
    if request.method == 'POST':
        passenger_id = request.POST.get('passenger')
        years = int(request.POST.get('years', 5))
        request.session['prediction_years'] = years  # Store in session
        if passenger_id:
            passenger = get_object_or_404(Passenger, pk=passenger_id)
            if not Prediction.objects.filter(passenger=passenger).exists():
                generate_predictions(request, passenger_id, years)
            return redirect('prediction_list', passenger_id=passenger_id)
    return redirect('home')

def generate_predictions(request, passenger_id, years = 5):
    passenger = get_object_or_404(Passenger, pk=passenger_id)
    flights = Flight.objects.filter(passenger=passenger, is_archived=False).order_by('date_time')
    
    if not flights:
        return redirect('prediction_list', passenger_id=passenger_id)
    
    dates = [f.date_time.date() for f in flights]
    times = [f.date_time.time() for f in flights]
    routes = [(f.departure_airport.code, f.arrival_airport.code) for f in flights]
    
    time_counts = Counter(times)
    most_common_time = time_counts.most_common(1)[0][0] if time_counts else None
    route_counts = Counter(routes)
    top_route = route_counts.most_common(1)[0][0] if route_counts else None
    dep_code, arr_code = top_route if top_route else (None, None)
    dep_airport = Airport.objects.filter(code=dep_code).first() if dep_code else None
    arr_airport = Airport.objects.filter(code=arr_code).first() if arr_code else None
    
    date_diffs = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
    avg_interval = sum(date_diffs) / len(date_diffs) if date_diffs else 30
    pattern_strength = min(len(flights) / 10, 1)
    base_percentage = 50 + (25 * pattern_strength)
    
    base_date = flights.last().date_time if flights else timezone.now()
    predictions = []
    fib_days = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]
    
    for i in range(1, 365 * years):
        pred_datetime = base_date + timedelta(days=i)
        if most_common_time:
            pred_datetime = pred_datetime.replace(hour=most_common_time.hour, minute=most_common_time.minute)

        percentage = base_percentage
        if i in fib_days:
            percentage += 5
            notes = f"Strong pattern; Fibonacci boost at day {i}"
        else:
            notes = f"Pattern-based at day {i}"
        percentage = min(percentage, 100)
        
        if i % int(avg_interval) == 0 or random.random() < 0.1:
            predictions.append(Prediction(
                passenger=passenger,
                predicted_date=pred_datetime,
                departure_airport=dep_airport,
                arrival_airport=arr_airport,
                percentage=percentage,
                notes=notes
            ))
    
    Prediction.objects.filter(passenger=passenger).delete()
    Prediction.objects.bulk_create(predictions)
    return redirect('prediction_list', passenger_id=passenger_id)

class AirportListView(ListView):
    model = Airport
    template_name = 'predictor/airport_list.html'

class AirportCreateView(CreateView):
    model = Airport
    form_class = AirportForm
    template_name = 'predictor/airport_form.html'
    success_url = reverse_lazy('airport_list')

class AirportUpdateView(UpdateView):
    model = Airport
    form_class = AirportForm
    template_name = 'predictor/airport_form.html'
    success_url = reverse_lazy('airport_list')

def archive_airport(request, pk):
    airport = get_object_or_404(Airport, pk=pk)
    airport.is_archived = True
    airport.save()
    return redirect('airport_list')

class PassengerListView(ListView):
    model = Passenger
    template_name = 'predictor/passenger_list.html'

class PassengerCreateView(CreateView):
    model = Passenger
    form_class = PassengerForm
    template_name = 'predictor/passenger_form.html'
    success_url = reverse_lazy('passenger_list')

class PassengerUpdateView(UpdateView):
    model = Passenger
    form_class = PassengerForm
    template_name = 'predictor/passenger_form.html'
    success_url = reverse_lazy('passenger_list')

def archive_passenger(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    passenger.is_archived = True
    passenger.save()
    return redirect('passenger_list')

class FlightListView(ListView):
    model = Flight
    template_name = 'predictor/flight_list.html'

class FlightCreateView(CreateView):
    model = Flight
    form_class = FlightForm
    template_name = 'predictor/flight_form.html'
    success_url = reverse_lazy('flight_list')

class FlightUpdateView(UpdateView):
    model = Flight
    form_class = FlightForm
    template_name = 'predictor/flight_form.html'
    success_url = reverse_lazy('flight_list')

def archive_flight(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    flight.is_archived = True
    flight.save()
    return redirect('flight_list')

class PredictionListView(ListView):
    model = Prediction
    template_name = 'predictor/prediction_list.html'
    
    def get_queryset(self):
        passenger_id = self.kwargs['passenger_id']
        passenger = get_object_or_404(Passenger, pk=passenger_id)
        years = self.request.session.get('prediction_years', 5)  # Get from session
        Prediction.objects.filter(passenger=passenger).delete()
        generate_predictions(None, passenger_id, years)
        return Prediction.objects.filter(passenger_id=passenger_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['passenger_id'] = self.kwargs['passenger_id']
        return context
    
def delete_predictions(request, passenger_id):
    passenger = get_object_or_404(Passenger, pk=passenger_id)
    Prediction.objects.filter(passenger=passenger).delete()
    return redirect('prediction_list', passenger_id=passenger_id)