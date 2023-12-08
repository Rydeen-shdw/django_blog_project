from typing import Optional, List

from weather.dto.city_dto import CityDTO, CreateCityDTO, CreateUserCityDTO, UserCityDTO
from weather.dto.country_dto import CountryDTO, CreateCountryDTO
from weather.models import City, Country, UserCity



class CountryDjangoORMRepository:
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


class CityDjangoORMRepository:
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



class UserCityDjangoORMRepository:
    def get_user_city(self, user, city) -> Optional[UserCityDTO]:
        user_city = user.cities.filter(city=city).first()
        if not user_city:
            return None
        return self._map_model_to_dto(user_city)

    def create_user_city(self, new_user_city_dto: CreateUserCityDTO) -> UserCityDTO:
        user_city = UserCity.objects.create(user_id=new_user_city_dto.user_id, city_id=new_user_city_dto.city_id)
        return self._map_model_to_dto(user_city)

    def get_user_cities(self, user) -> list[CityDTO]:
        user_cities = user.cities.all()
        return [self._map_city_model_to_dto(user_city.city) for user_city in user_cities]

    def get_user_city_by_slug(self, slug) -> Optional[CityDTO]:
        user_city = City.objects.get(slug=slug)
        if not user_city:
            return None
        return self._map_city_model_to_dto(user_city)

    def _map_model_to_dto(self, user_city) -> UserCityDTO:
        return UserCityDTO(
            id=user_city.user.id,
            user_id=user_city.user_id,
            city_id=user_city.city_id,
            create_at=user_city.create_at
        )

    def _map_city_model_to_dto(self, city) -> CityDTO:
        return CityDTO(
            id=city.pk,
            name=city.name,
            slug=city.slug,
            description=city.description,
            image=city.image,
            lat=city.lat,
            lon=city.lon,
            country_id=city.country.pk
        )


