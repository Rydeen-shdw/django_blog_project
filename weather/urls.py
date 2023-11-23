from django.urls import path

from weather import views

app_name = 'weather'


urlpatterns = [
    path('', views.get_city_name_view, name='weather_city'),
    path('<str:city>/forecast/', views.weather_forecast_view, name='weather_forecast'),
]