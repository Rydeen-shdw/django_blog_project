from datetime import datetime
from requests.exceptions import HTTPError

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from weather import forms
from weather import services


@require_http_methods(['POST', "GET"])
def get_city_name_view(request):
    if request.method == 'POST':
        form = forms.CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city_name']
            return redirect('weather:weather_forecast', city=city)
    else:
        form = forms.CityForm()

    return render(request, 'weather/city_search.html', {'form': form})


def weather_forecast_view(request, city):
    time_now = datetime.now()
    current_time = time_now.strftime("%H:%M")
    try:
        data = services.get_weather(city=city)
        context = {
            'city': city,
            'weather_data': data,
            'current_time': current_time
        }
        return render(request, 'weather/weather_detail.html', context)
    except HTTPError as err404:
        if err404.response.status_code == 404:
            messages.error(request, f"Weather data for {city} not found.")
            return redirect('weather:weather_city')
    except Exception as e:
        messages.error(request, f"An error occurred")
        return redirect('weather:weather_city')

