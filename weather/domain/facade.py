from django.utils.text import slugify

from weather.domain.interfaces.facade_interfaces import CityCountryFacadeInterface
from weather.domain.interfaces.repository_interfaces import CountryRepositoryInterface, CityRepositoryInterface, \
    UserCityRepositoryInterface
from weather.domain.interfaces.service_interfaces import CountriesServiceInterface, WikiServiceInterface
from weather.dto.city_dto import CreateCityDTO, CityDTO
from weather.dto.country_dto import CreateCountryDTO, CountryDTO
from weather.exceptions import (
    ServerReturnInvalidStatusCode,
    ServerInvalidResponseError,
    CountryServiceUnavailable,
    PageNotFoundError,
    WikiServiceUnavailable, UserCityAlreadyExist)


class CityCountryFacade(CityCountryFacadeInterface):
    def __init__(self,
                 country_repository: CountryRepositoryInterface,
                 city_repository: CityRepositoryInterface,
                 user_city_repository: UserCityRepositoryInterface,
                 country_service: CountriesServiceInterface,
                 wiki_service: WikiServiceInterface):
        self._country_repository = country_repository
        self._city_repository = city_repository
        self._user_city_repository = user_city_repository
        self._country_service = country_service
        self._wiki_service = wiki_service

    def add_city_to_user_favorites(self, user_id: int, country_code: str, city_name: str, lat: float, lon: float) -> bool:
        country = self._country_repository.get_country_by_code(country_code)

        if country is None:
            country = self._get_country_data_or_raise(country_code)

        city = self._city_repository.get_city_by_name(city_name)

        if not city:
            city = self._get_city_data_or_raise(city_name, country.id, lat, lon)

        if self._user_city_repository.is_user_city_exist(user_id, city.id):
            raise UserCityAlreadyExist('City already added to current user')

        self._user_city_repository.create_user_city(user_id, city.id)

        return True

    def _get_city_data_or_raise(self, city_name: str, country_id,lat: float, lon: float) -> CityDTO:
        city_wiki_service_dto = self._wiki_service.get_wiki_page(city_name)
        new_city_dto = CreateCityDTO(
            name=city_name,
            slug=slugify(city_name),
            description=city_wiki_service_dto.description,
            image=city_wiki_service_dto.image,
            lat=lat,
            lon=lon,
            country_id=country_id
        )
        city = self._city_repository.create_city(new_city_dto)
        return city

    def _get_country_data_or_raise(self, country_code: str) -> CountryDTO:
        try:
            country_service_dto = self._country_service.get_country_by_code(country_code)
        except (ServerInvalidResponseError, ServerReturnInvalidStatusCode) as exception:
            raise CountryServiceUnavailable(str(exception))

        try:
            country_wiki_service_dto = self._wiki_service.get_wiki_page(country_service_dto.name)
        except (ServerInvalidResponseError, ServerReturnInvalidStatusCode, PageNotFoundError) as exception:
            raise WikiServiceUnavailable(str(exception))

        new_country_dto = CreateCountryDTO(
            name=country_service_dto.name,
            slug=slugify(country_service_dto.name),
            code=country_service_dto.code,
            population=country_service_dto.population,
            capital=country_service_dto.capital,
            description=country_wiki_service_dto.description,
            flag=country_wiki_service_dto.image
        )
        country = self._country_repository.create_country(new_country_dto)
        return country
