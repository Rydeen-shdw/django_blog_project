import requests

from weather.dto.wiki_dto import WikiServiceDTO
from weather.exceptions import ServerConnectionError, ServerInvalidResponseError, ServerReturnInvalidStatusCode, \
    PageNotFoundError


class WikiService:
    _WIKI_API_ROOT_URL = 'http://en.wikipedia.org/w/api.php?action=query&' \
                         'titles={query}&prop=extracts|pageimages&format=json&pithumbsize=1000'

    def get_wiki_page(self, query: str) -> WikiServiceDTO:
        response_json, status_code = self._get_page_data_from_api(query)
        self._validate_response_or_raise(response_json, status_code)
        page_dto = self._parse_response_json(response_json)
        return page_dto

    def _get_page_data_from_api(self, query: str) -> tuple[dict, int]:
        url = self._WIKI_API_ROOT_URL.format(query=query)

        try:
            response = requests.get(url, timeout=(2, 2))
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            raise ServerConnectionError('WikiPedia connection error')

        response_json = response.json()
        status_code = response.status_code
        return response_json, status_code

    def _validate_response_or_raise(self, response_json: dict, status_code: int) -> None:
        if response_json is None:
            raise ServerInvalidResponseError(f'WikiPedia internal server error, status code: {status_code}')

        if status_code != 200:
            raise ServerReturnInvalidStatusCode(f'WikiPedia return invalid status code, status code: {status_code}')

        page = response_json['query']['pages']
        print(page)
        if '-1' in page:
            raise PageNotFoundError('WikiPedia page not found')

    def _parse_response_json(self, response_json: dict) -> WikiServiceDTO:
        page = response_json['query']['pages']
        _, page_info = next(iter(page.items()))

        description = page_info['extract']
        image = page_info['thumbnail']['source'] if 'thumbnail' in page_info else ''

        page_dto = WikiServiceDTO(
            description=description,
            image=image
        )
        return page_dto


if __name__ == '__main__':
    wiki_service = WikiService()
    page = wiki_service.get_wiki_page('France')
    print(page)

