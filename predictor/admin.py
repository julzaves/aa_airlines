from django.contrib import admin
from .models import Airport, Passenger, Flight, Prediction

admin.site.register(Airport)
admin.site.register(Passenger)
admin.site.register(Flight)
admin.site.register(Prediction)