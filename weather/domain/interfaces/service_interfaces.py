from abc import ABCMeta, abstractmethod

from weather.dto.country_dto import CountryServiceDTO
from weather.dto.wiki_dto import WikiServiceDTO


class CountriesServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_country_by_code(self, code: str) -> CountryServiceDTO:
        pass


class WeatherTodayServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_weather(self, city: str):
        pass


class WikiServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_wiki_page(self, query: str) -> WikiServiceDTO:
        pass
