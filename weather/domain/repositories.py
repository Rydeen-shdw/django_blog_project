from typing import Optional

from weather.domain.interfaces.repository_interfaces import CountryRepositoryInterface, CityRepositoryInterface, \
    UserCityRepositoryInterface
from weather.dto.city_dto import CityDTO, CreateCityDTO
from weather.dto.country_dto import CountryDTO, CreateCountryDTO
from weather.models import City, Country, UserCity


class CountryDjangoORMRepository(CountryRepositoryInterface):
    def get_country_by_code(self, country_code: str) -> Optional[CountryDTO]:
        country = Country.objects.filter(code=country_code).first()
        if not country:
            return None
        return self._map_model_to_dto(country)

    def create_country(self, new_country_dto: CreateCountryDTO) -> CountryDTO:
        country = Country.objects.create(**new_country_dto._asdict())
        return self._map_model_to_dto(country)

    def _map_model_to_dto(self, country: Country) -> CountryDTO:
        country_dto = CountryDTO(
            id=country.pk,
            name=country.name,
            slug=country.slug,
            code=country.code,
            population=country.population,
            description=country.description,
            flag=country.flag,
            capital=country.capital
        )
        return country_dto


class CityDjangoORMRepository(CityRepositoryInterface):
    def get_city_by_name(self, city_name: str) -> Optional[CityDTO]:
        city = City.objects.filter(name=city_name).first()
        if not city:
            return None
        return self._map_model_to_dto(city)

    def create_city(self, new_city_dto: CreateCityDTO) -> CityDTO:
        city = City.objects.create(**new_city_dto._asdict())
        return self._map_model_to_dto(city)

    def _map_model_to_dto(self, city: City) -> CityDTO:
        city_dto = CityDTO(
            id=city.pk,
            name=city.name,
            slug=city.slug,
            description=city.description,
            image=city.image,
            lat=city.lat,
            lon=city.lon,
            country_id=city.country.pk
        )
        return city_dto


class UserCityDjangoORMRepository(UserCityRepositoryInterface):
    def is_user_city_exist(self, user_id: int, city_id: int) -> bool:
        user_city = UserCity.objects.filter(user_id=user_id, city_id=city_id).exists()
        return user_city

    def create_user_city(self, user_id: int, city_id: int) -> None:
        UserCity.objects.create(user_id=user_id, city_id=city_id)

