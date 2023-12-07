import logging

from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.contrib import messages

from weather.forms import CityWeatherForm
from weather.services.weather_services import OpenWeatherTodayService
from weather.exceptions import CityNotFoundError, ServerInvalidResponseError, ServerReturnInvalidStatusCode

logger = logging.getLogger('weather')


class WeatherCityView(View):
    def get(self, request):
        form = CityWeatherForm()
        return render(request, 'weather/today.html', {'form': form})

    def post(self, request):
        form = CityWeatherForm(request.POST)

        if form.is_valid():
            api_key = settings.WEATHER_API_KEY
            city = form.cleaned_data['city']

            weather_service = OpenWeatherTodayService(api_key)

            try:
                city_weather = weather_service.get_weather(city)
            except CityNotFoundError as exception:
                messages.warning(request, str(exception))
                return redirect('weather:today')
            except (ServerInvalidResponseError, ServerReturnInvalidStatusCode) as exception:
                messages.error(request, 'External weather service error')
                logger.error(str(exception))
                return redirect('weather:today')
            return render(request, 'weather/today.html', {'form': form, 'weather': city_weather})

        return render(request, 'weather/today.html', {'form': form})




