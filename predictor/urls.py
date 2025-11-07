from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('select_passenger/', views.select_passenger_for_predictions, name='select_passenger'),
    path('airports/', views.AirportListView.as_view(), name='airport_list'),
    path('airports/create/', views.AirportCreateView.as_view(), name='airport_create'),
    path('airports/<int:pk>/update/', views.AirportUpdateView.as_view(), name='airport_update'),
    path('airports/<int:pk>/archive/', views.archive_airport, name='airport_archive'),
    path('passengers/', views.PassengerListView.as_view(), name='passenger_list'),
    path('passengers/create/', views.PassengerCreateView.as_view(), name='passenger_create'),
    path('passengers/<int:pk>/update/', views.PassengerUpdateView.as_view(), name='passenger_update'),
    path('passengers/<int:pk>/archive/', views.archive_passenger, name='passenger_archive'),
    path('flights/', views.FlightListView.as_view(), name='flight_list'),
    path('flights/create/', views.FlightCreateView.as_view(), name='flight_create'),
    path('flights/<int:pk>/update/', views.FlightUpdateView.as_view(), name='flight_update'),
    path('flights/<int:pk>/archive/', views.archive_flight, name='flight_archive'),
    path('predictions/<int:passenger_id>/', views.PredictionListView.as_view(), name='prediction_list'),
    path('predictions/<int:passenger_id>/delete/', views.delete_predictions, name='delete_predictions'),
]