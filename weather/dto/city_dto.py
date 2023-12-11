from typing import NamedTuple


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
