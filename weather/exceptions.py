class CityNotFoundError(BaseException):
    pass


class PageNotFoundError(BaseException):
    pass


class ServerInvalidResponseError(BaseException):
    pass


class ServerReturnInvalidStatusCode(BaseException):
    pass


class ServerConnectionError(BaseException):
    pass
