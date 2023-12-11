from abc import ABCMeta, abstractmethod
from typing import Optional

from weather.dto.city_dto import CityDTO, CreateCityDTO
from weather.dto.country_dto import CountryDTO, CreateCountryDTO


class CountryRepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_country_by_code(self, country_code: str) -> Optional[CountryDTO]:
        pass

    @abstractmethod
    def create_country(self, new_country_dto: CreateCountryDTO) -> CountryDTO:
        pass


class CityRepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_city_by_name(self, city_name: str) -> Optional[CityDTO]:
        pass

    @abstractmethod
    def create_city(self, new_city_dto: CreateCityDTO) -> CityDTO:
        pass


class UserCityRepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def is_user_city_exist(self, user_id: int, city_id: int) -> bool:
        pass

    @abstractmethod
    def create_user_city(self, user_id: int, city_id: int) -> None:
        pass
