from http import HTTPStatus


class CustomException(Exception):
    code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


class HttpStatusException(CustomException):
    def __init__(self, http_status: HTTPStatus, message=None):
        self.code = http_status
        self.error_code = http_status
        self.message = message or http_status.description
        super().__init__(self.message)


# Specific exceptions
class BadRequestException(HttpStatusException):
    def __init__(self, message=None):
        super().__init__(HTTPStatus.BAD_REQUEST, message)


class NotFoundException(HttpStatusException):
    def __init__(self, message=None):
        super().__init__(HTTPStatus.NOT_FOUND, message)


class ForbiddenException(HttpStatusException):
    def __init__(self, message=None):
        super().__init__(HTTPStatus.FORBIDDEN, message)


class UnauthorizedException(HttpStatusException):
    def __init__(self, message=None):
        super().__init__(HTTPStatus.UNAUTHORIZED, message)


class UnprocessableException(HttpStatusException):
    def __init__(self, message=None):
        super().__init__(HTTPStatus.UNPROCESSABLE_ENTITY, message)


class DuplicateValueException(HttpStatusException):
    def __init__(self, message=None):
        super().__init__(HTTPStatus.UNPROCESSABLE_ENTITY, message)
