
import requests
from datetime import datetime

from django.conf import settings


def get_weather_data(city):
    connect_timeout = 5

    key = settings.OPENWEATHERMAP_API_KEY
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'units': 'metric',
        'appid': key,
    }
    response = requests.get(url, params=params, timeout=connect_timeout )
    response.raise_for_status()
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return None

def get_weather(city):
    data = get_weather_data(city)
    if data:
        data = {
            'temp': data["main"]["temp"],
            'icon': data["weather"][0]["icon"],
            'weather': data["weather"][0]["description"],
            'wind_speed': data["wind"]["speed"] * 3.6,
            'humidity': data["main"]["humidity"],
            'time': data["timezone"],
            'sunrise': datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime('%H')
        }
        return data
    return None

