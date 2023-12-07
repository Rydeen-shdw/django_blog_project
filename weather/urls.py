from django.urls import path

from weather import views

app_name = 'weather'


urlpatterns = [
    path('today/', views.WeatherCityView.as_view(), name='today'),
]
