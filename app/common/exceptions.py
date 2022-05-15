from http import HTTPStatus


class BaseAPIException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

    def to_dict(self):
        return {"message": self.message, "error_code": self.error_code}


class NotFoundException(BaseAPIException):
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.NOT_FOUND)


class BadRequestException(BaseAPIException):
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.BAD_REQUEST)


class DataAlreadyExists(BaseAPIException):
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.CONFLICT)
