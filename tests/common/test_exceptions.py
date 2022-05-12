import pytest
from http import HTTPStatus

from app.common.exceptions import (
    BaseAPIException,
    BadRequestException,
    NotFoundException,
)


def test_base_api_exception():
    with pytest.raises(BaseAPIException):
        raise BaseAPIException("message", HTTPStatus.BAD_REQUEST)


def test_base_api_exception_to_dict():
    exception = BaseAPIException("message", HTTPStatus.BAD_REQUEST)
    exc_dict = exception.to_dict()
    assert exc_dict["message"] == "message"
    assert exc_dict["error_code"] == HTTPStatus.BAD_REQUEST


def test_bad_request_exception():
    with pytest.raises(BadRequestException):
        raise BadRequestException("message")


def test_bad_request_exception_to_dict():
    exception = BadRequestException("message")
    exc_dict = exception.to_dict()
    assert exc_dict["message"] == "message"
    assert exc_dict["error_code"] == HTTPStatus.BAD_REQUEST


def test_not_found_exception():
    with pytest.raises(NotFoundException):
        raise NotFoundException("message")


def test_not_found_exception_to_dict():
    exception = NotFoundException("message")
    exc_dict = exception.to_dict()
    assert exc_dict["message"] == "message"
    assert exc_dict["error_code"] == HTTPStatus.NOT_FOUND
