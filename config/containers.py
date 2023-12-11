from dependency_injector import containers, providers

from weather.domain.interfaces.repository_interfaces import (
    CountryRepositoryInterface,
    CityRepositoryInterface,
    UserCityRepositoryInterface
)
from weather.domain.interfaces.service_interfaces import WikiServiceInterface, CountriesServiceInterface
from weather.domain.interfaces.facade_interfaces import CityCountryFacadeInterface
from weather.domain.repositories import CountryDjangoORMRepository, CityDjangoORMRepository, UserCityDjangoORMRepository
from weather.domain.services.wiki_service import WikiService
from weather.domain.services.country_services import RestCountriesService
from weather.domain.facade import CityCountryFacade


class RepositoryContainer(containers.DeclarativeContainer):
    country_repository: providers.Provider[CountryRepositoryInterface] = providers.Factory(
        CountryDjangoORMRepository
    )
    city_repository: providers.Provider[CityRepositoryInterface] = providers.Factory(
        CityDjangoORMRepository
    )
    user_city_repository: providers.Provider[UserCityRepositoryInterface] = providers.Factory(
        UserCityDjangoORMRepository
    )


class ServiceContainer(containers.DeclarativeContainer):
    wiki_service: providers.Provider[WikiServiceInterface] = providers.Factory(WikiService)
    country_service: providers.Provider[CountriesServiceInterface] = providers.Factory(RestCountriesService)


class FacadeContainer(containers.DeclarativeContainer):
    city_country_facade: providers.Provider[CityCountryFacadeInterface] = providers.Factory(
        CityCountryFacade,
        country_repository=RepositoryContainer.country_repository,
        city_repository=RepositoryContainer.city_repository,
        user_city_repository=RepositoryContainer.user_city_repository,
        country_service=ServiceContainer.country_service,
        wiki_service=ServiceContainer.wiki_service
    )
