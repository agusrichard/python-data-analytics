import pytest
from unittest import mock

from app.common.file import renaming_file
from app.common.file import create_file_uploader
from app.common.exceptions import BadRequestException

FILENAME_TEST = "test.mp3"


def test_positive_renaming_file():
    filename = FILENAME_TEST
    assert renaming_file(filename) is not None


def test_negative_renaming_file_no_extension():
    filename = "test"
    with pytest.raises(BadRequestException):
        renaming_file(filename)


def test_negative_renaming_file_none():
    filename = None
    with pytest.raises(BadRequestException):
        renaming_file(filename)


@mock.patch("app.common.file.boto3")
def test_positive_create_file_uploader(mock_boto3):
    mock_s3 = mock.MagicMock()
    mock_boto3.client.return_value = mock_s3
    mock_s3.upload_fileobj.return_value = "https://test.com/test.mp3"

    config = {
        "AWS_ACCESS_KEY": "test",
        "AWS_ACCESS_SECRET": "test",
        "S3_BUCKET_NAME": "test",
        "S3_BUCKET_BASE_URL": "https://test.com",
    }
    mocked_app = mock.MagicMock()
    mocked_app.config.__getitem__.side_effect = config.__getitem__

    mocked_file = mock.MagicMock()
    mocked_file.filename = FILENAME_TEST
    mocked_file.content_type = "audio/mpeg"

    uploader = create_file_uploader(mocked_app)
    assert uploader is not None
    assert uploader(mocked_file) == "https://test.com/test.mp3"


@mock.patch("app.common.file.boto3")
def test_negative_create_file_uploader_upload_raise_exception(mock_boto3):
    mock_s3 = mock.MagicMock()
    mock_boto3.client.return_value = mock_s3
    mock_s3.upload_fileobj.side_effect = Exception("test upload error")

    config = {
        "AWS_ACCESS_KEY": "test",
        "AWS_ACCESS_SECRET": "test",
        "S3_BUCKET_NAME": "test",
        "S3_BUCKET_BASE_URL": "https://test.com",
    }
    mocked_app = mock.MagicMock()
    mocked_app.config.__getitem__.side_effect = config.__getitem__

    mocked_file = mock.MagicMock()
    mocked_file.filename = FILENAME_TEST
    mocked_file.content_type = "audio/mpeg"

    uploader = create_file_uploader(mocked_app)
    assert uploader is not None
    with pytest.raises(Exception):
        uploader(mocked_file)
