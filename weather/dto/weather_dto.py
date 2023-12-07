from typing import NamedTuple


class CoordinatesDTO(NamedTuple):
    lat: float
    lon: float


class WeatherTimeInfoDTO(NamedTuple):
    current: str
    sunrise: str
    sunset: str


class WeatherTodayDTO(NamedTuple):
    city: str
    country_code: str
    coordinates: CoordinatesDTO
    temperature: int
    humidity: int
    condition: str
    wind_speed: int
    icon: str
    time_info: WeatherTimeInfoDTO

