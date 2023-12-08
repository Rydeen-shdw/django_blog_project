from django.shortcuts import redirect
from django.contrib import messages
from django.utils.text import slugify

from weather.services.country_services import RestCountriesService
from weather.services.wiki_service import WikiService
from weather.dto.country_dto import CreateCountryDTO
from weather.dto.city_dto import CreateCityDTO, CreateUserCityDTO
from weather.repositories import CountryDjangoORMRepository, CityDjangoORMRepository, UserCityDjangoORMRepository


class WeatherFacade:
    def __init__(self):
        self.wiki_service = WikiService()
        self.country_repository = CountryDjangoORMRepository()
        self.city_repository = CityDjangoORMRepository()
        self.user_city_repository = UserCityDjangoORMRepository()
        self.country_service = RestCountriesService()

    def create_or_get_country(self, country_code):
        country = self.country_repository.get_country_by_code(country_code)

        if not country:
            country_service_dto = self.country_service.get_country_by_code(country_code)
            country_wiki_service_dto = self.wiki_service.get_wiki_page(country_service_dto.name)

            new_country_dto = CreateCountryDTO(
                name=country_service_dto.name,
                slug=slugify(country_service_dto.name),
                code=country_service_dto.code,
                population=country_service_dto.population,
                capital=country_service_dto.capital,
                description=country_wiki_service_dto.description,
                flag=country_wiki_service_dto.image
            )

            country = self.country_repository.create_country(new_country_dto)

        return country

    def create_or_get_city(self, city_name, country, lat, lon):
        city = self.city_repository.get_city_by_name(city_name)

        if not city:
            city_wiki_service_dto = self.wiki_service.get_wiki_page(city_name)
            new_city_dto = CreateCityDTO(
                name=city_name,
                slug=slugify(city_name),
                description=city_wiki_service_dto.description,
                image=city_wiki_service_dto.image,
                lat=lat,
                lon=lon,
                country_id=country.id
            )

            city = self.city_repository.create_city(new_city_dto)

        return city

    def add_user_city(self, request, user, city):
        existing_user_city = self.user_city_repository.get_user_city(user=user, city=city)
        if existing_user_city:
            messages.warning(request,f'City "{city.name}" is already added.')
            return redirect('weather:today')

        new_user_city_dto = CreateUserCityDTO(user_id=user.id, city_id=city.id)
        self.user_city_repository.create_user_city(new_user_city_dto)

        return redirect('blog:post_list')