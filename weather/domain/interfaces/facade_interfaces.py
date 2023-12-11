from abc import ABCMeta, abstractmethod


class CityCountryFacadeInterface(metaclass=ABCMeta):
    @abstractmethod
    def add_city_to_user_favorites(self, user_id: int, country_code: str, city_name: str, lat: float, lon: float) -> bool:
        pass

