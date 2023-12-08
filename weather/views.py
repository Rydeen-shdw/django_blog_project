import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.contrib import messages

from weather.dto.city_dto import CreateCityDTO, CreateUserCityDTO
from weather.dto.country_dto import CreateCountryDTO
from weather.forms import CityWeatherForm, UserCityCreateForm
from weather.services.country_services import RestCountriesService
from weather.services.weather_services import OpenWeatherTodayService
from weather.exceptions import CityNotFoundError, ServerInvalidResponseError, ServerReturnInvalidStatusCode
from weather.repositories import CountryDjangoORMRepository, CityDjangoORMRepository, UserCityDjangoORMRepository
from weather.services.wiki_service import WikiService
from weather.facade import WeatherFacade

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
        form = UserCityCreateForm(request.POST)

        if form.is_valid():
            city_name = request.POST.get('city')
            country_code = request.POST.get('country_code')
            lat = float(request.POST.get('lat'))
            lon = float(request.POST.get('lon'))

            facade = WeatherFacade()

            country = facade.create_or_get_country(country_code)
            city = facade.create_or_get_city(city_name, country, lat, lon)

            user = request.user
            return facade.add_user_city(request,user, city)
        else:
            messages.error(request, 'Invalid data received')
            return redirect('weather:today')


class UserCityListView(LoginRequiredMixin, View):
    def get(self, request):
        user_city_repository = UserCityDjangoORMRepository()
        user_cities = user_city_repository.get_user_cities(request.user)
        return render(request, 'weather/user_cities_list.html', {'cities': user_cities})

class UserCityDetailView(LoginRequiredMixin, View):
    def get(self, request, slug):
        user_city_repository = UserCityDjangoORMRepository()
        user_city = user_city_repository.get_user_city_by_slug(slug)
        return render(request, 'weather/user_city_detail.html', {'user_city': user_city})
