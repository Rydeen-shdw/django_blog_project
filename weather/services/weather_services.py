import requests
from datetime import datetime
from abc import ABCMeta, abstractmethod

from weather.exceptions import CityNotFoundError, ServerInvalidResponseError, ServerReturnInvalidStatusCode
from weather.dto.weather_dto import CoordinatesDTO, WeatherTimeInfoDTO, WeatherTodayDTO


class WeatherTodayServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_weather(self, city: str):
        pass


class OpenWeatherTodayService(WeatherTodayServiceInterface):
    _WEATHER_API_ROOT_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    def __init__(self, api_key: str):
        self._api_key = api_key

    def get_weather(self, city: str) -> WeatherTodayDTO:
        response_json, status_code = self._get_weather_data_from_api(city)
        self._validate_response_or_raise(response_json, status_code)
        weather_today_dto = self._parse_response_json(response_json)
        return weather_today_dto

    def _get_weather_data_from_api(self, city: str) -> tuple[dict, int]:
        weather_api_url = self._WEATHER_API_ROOT_URL.format(city=city, api_key=self._api_key)
        response = requests.get(weather_api_url)
        response_json = response.json()
        status_code = response.status_code
        return response_json, status_code

    def _validate_response_or_raise(self, response_json: dict, status_code: int) -> None:
        if response_json is None:
            raise ServerInvalidResponseError(f'OpenWeather internal server error, status code: {status_code}')

        if status_code != 200:
            if status_code == 404:
                raise CityNotFoundError(response_json['message'].capitalize())
            raise ServerReturnInvalidStatusCode(f'OpenWeather return invalid status code, status code: {status_code}')

    def _parse_response_json(self, response_json: dict) -> WeatherTodayDTO:
        city = response_json['name']
        country_code = response_json['sys']['country']
        coordinates = CoordinatesDTO(lat=response_json['coord']['lat'],
                                     lon=response_json['coord']['lon'])

        temperature = int(response_json['main']['temp'])
        humidity = response_json['main']['humidity']
        condition = response_json['weather'][0]['main']
        icon = response_json['weather'][0]['icon']
        wind_speed = int(response_json['wind']['speed'])

        time_info = WeatherTimeInfoDTO(
            current=datetime.fromtimestamp(response_json['dt']).strftime('%H:%M'),
            sunrise=datetime.utcfromtimestamp(
                response_json['sys']['sunrise'] + response_json['timezone']).strftime('%H:%M'),
            sunset=datetime.utcfromtimestamp(
                response_json['sys']['sunset'] + response_json['timezone']).strftime('%H:%M')
        )

        weather_today_dto = WeatherTodayDTO(
            city=city,
            country_code=country_code,
            coordinates=coordinates,
            temperature=temperature,
            humidity=humidity,
            condition=condition,
            icon=icon,
            wind_speed=wind_speed,
            time_info=time_info
        )
        return weather_today_dto
