import pytest
from unittest import mock
from werkzeug.datastructures import FileStorage

from app.common.exceptions import BadRequestException
from app.common.file import (
    renaming_file,
    create_file_uploader,
    process_files_to_streams,
)

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
    mock_s3.upload_fileobj.return_value = f"https://test.com/{FILENAME_TEST}"

    config = {
        "AWS_ACCESS_KEY": "test",
        "AWS_ACCESS_SECRET": "test",
        "S3_BUCKET_NAME": "test",
        "S3_BUCKET_BASE_URL": "https://test.com",
    }
    mocked_app = mock.MagicMock()
    mocked_app.config.__getitem__.side_effect = config.__getitem__

    data = {
        "stream": "test",
        "filename": FILENAME_TEST,
        "content_type": "audio/mp3",
    }

    uploader = create_file_uploader(mocked_app)
    assert uploader is not None
    assert uploader(data) == f"https://test.com/{FILENAME_TEST}"


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


@mock.patch("app.common.file.base64")
def test_positive_process_files_to_streams(mocked_base64):
    mocked_base64.b64encode.return_value = "test"

    files = {
        "song_file": FileStorage(None, FILENAME_TEST),
        "small_thumbnail_file": FileStorage(None, "test.png"),
        "large_thumbnail_file": FileStorage(None, "test.png"),
    }

    result = process_files_to_streams(files)
    assert result is not None
    assert result["song_file"] is not None
    assert result["small_thumbnail_file"] is not None
    assert result["large_thumbnail_file"] is not None


@mock.patch("app.common.file.base64")
def test_positive_process_files_to_streams_skip_invalid_file(mocked_base64):
    mocked_base64.b64encode.return_value = "test"

    files = {
        "song_file": FileStorage(None, FILENAME_TEST),
        "small_thumbnail_file": FileStorage(None, ""),
        "large_thumbnail_file": FileStorage(None, ""),
    }

    result = process_files_to_streams(files)
    assert result is not None
    assert result["song_file"] is not None
