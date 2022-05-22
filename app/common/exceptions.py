from http import HTTPStatus

from app.common.messages import FAILED_TO_UPLOAD


class BaseAPIException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

    def __str__(self):
        return self.message

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


class UploadFailedException(BaseAPIException):
    def __init__(self):
        super().__init__(FAILED_TO_UPLOAD, HTTPStatus.INTERNAL_SERVER_ERROR)


class FieldRequired(BaseAPIException):
    def __init__(self, field_name: str):
        message = f"{field_name} is required"
        super().__init__(message, HTTPStatus.BAD_REQUEST)
