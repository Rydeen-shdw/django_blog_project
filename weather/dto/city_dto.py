from typing import NamedTuple
from datetime import datetime


class CityDTO(NamedTuple):
    id: int
    name: str
    slug: str
    description: str
    image: str
    lat: float
    lon: float
    country_id: int


class CreateCityDTO(NamedTuple):
    name: str
    slug: str
    description: str
    image: str
    lat: float
    lon: float
    country_id: int



class CreateUserCityDTO(NamedTuple):
    user_id: int
    city_id: int


class UserCityDTO(NamedTuple):
    id: int
    user_id: int
    city_id: int
    create_at: datetime



