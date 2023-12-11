class CityNotFoundError(BaseException):
    pass


class CountryNotFoundError(BaseException):
    pass


class PageNotFoundError(BaseException):
    pass


class ServerInvalidResponseError(BaseException):
    pass


class ServerReturnInvalidStatusCode(BaseException):
    pass


class ServerConnectionError(BaseException):
    pass


class CountryServiceUnavailable(BaseException):
    pass


class WikiServiceUnavailable(BaseException):
    pass


class UserCityAlreadyExist(BaseException):
    pass
