import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.contrib import messages

from weather.forms import CityWeatherForm
from weather.domain.services.weather_services import OpenWeatherTodayService
from weather.exceptions import (
    CityNotFoundError,
    ServerInvalidResponseError,
    ServerReturnInvalidStatusCode,
    CountryServiceUnavailable,
    WikiServiceUnavailable, UserCityAlreadyExist)
from config.containers import FacadeContainer

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


class UserCityCreateView(LoginRequiredMixin, View):
    def post(self, request):
        city_name = request.POST.get('city')
        country_code = request.POST.get('country_code')
        lat = float(request.POST.get('lat'))
        lon = float(request.POST.get('lon'))

        city_country_facade = FacadeContainer.city_country_facade()

        try:
            city_country_facade.add_city_to_user_favorites(request.user.pk, country_code, city_name, lat, lon)
        except UserCityAlreadyExist as exception:
            messages.error(request, str(exception))
            return redirect('blog:post_list')
        except (CountryServiceUnavailable, WikiServiceUnavailable) as exception:
            logger.error(str(exception))
            messages.error(request, 'Something went wrong, try it later')
            return redirect('blog:post_list')

        messages.success(request, f'City {city_name} added to user: {request.user}, favorites')
        return redirect('blog:post_list')

