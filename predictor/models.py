from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Passenger(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Flight(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    departure_airport = models.ForeignKey(Airport, related_name='departures', on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey(Airport, related_name='arrivals', on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.passenger.name}: {self.departure_airport.code} to {self.arrival_airport.code} on {self.date_time}"

class Prediction(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    predicted_date = models.DateTimeField()
    departure_airport = models.ForeignKey(Airport, related_name='predicted_departures', on_delete=models.CASCADE, null=True, blank=True)
    arrival_airport = models.ForeignKey(Airport, related_name='predicted_arrivals', on_delete=models.CASCADE, null=True, blank=True)
    percentage = models.FloatField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Prediction for {self.passenger.name} on {self.predicted_date}: {self.percentage}%"