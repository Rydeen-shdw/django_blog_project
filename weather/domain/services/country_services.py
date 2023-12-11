import requests

from weather.domain.interfaces.service_interfaces import CountriesServiceInterface
from weather.dto.country_dto import CountryServiceDTO
from weather.exceptions import ServerConnectionError, ServerInvalidResponseError, ServerReturnInvalidStatusCode


class RestCountriesService(CountriesServiceInterface):
    _COUNTRIES_API_ROOT_URL = 'https://restcountries.com/v3.1/alpha/{code}'

    def get_country_by_code(self, code: str) -> CountryServiceDTO:
        response_json, status_code = self._get_country_data_from_api(code)
        self._validate_response_or_raise(response_json, status_code)
        country_dto = self._parse_response_json(response_json)
        return country_dto

    def _get_country_data_from_api(self, code: str) -> tuple[dict, int]:
        url = self._COUNTRIES_API_ROOT_URL.format(code=code)

        try:
            response = requests.get(url, timeout=(2, 2))
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            raise ServerConnectionError('RestCountries connection error')

        response_json = response.json()
        status_code = response.status_code
        return response_json, status_code

    def _validate_response_or_raise(self, response_json: dict, status_code: int) -> None:
        if response_json is None:
            raise ServerInvalidResponseError(f'RestCountries internal server error, status code: {status_code}')

        if status_code != 200:
            raise ServerReturnInvalidStatusCode(f'RestCountries return invalid status code, status code: {status_code}')

    def _parse_response_json(self, response_json: dict) -> CountryServiceDTO:
        name = response_json[0]['name']['common']
        code = response_json[0]['cca2']
        capital = response_json[0]['capital'][0]
        population = response_json[0]['population']
        country_dto = CountryServiceDTO(
            name=name,
            code=code,
            capital=capital,
            population=population,
        )
        return country_dto


if __name__ == '__main__':
    country_service = RestCountriesService()
    country = country_service.get_country_by_code('UA')
    print(country)
