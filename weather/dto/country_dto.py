from typing import NamedTuple


class CountryServiceDTO(NamedTuple):
    name: str
    code: str
    capital: str
    population: int


class CountryDTO(NamedTuple):
    id: int
    name: str
    slug: str
    code: str
    population: int
    description: str
    flag: str
    capital: str


class CreateCountryDTO(NamedTuple):
    name: str
    slug: str
    code: str
    population: int
    description: str
    flag: str
    capital: str
