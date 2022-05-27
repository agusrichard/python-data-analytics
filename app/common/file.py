import io
import boto3
import base64
from flask import Flask
from typing import Callable
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from app.common.messages import INVALID_FILENAME
from app.common.exceptions import UploadFailedException, BadRequestException


def create_file_uploader(app: Flask) -> Callable:
    """
    Create a file uploader
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=app.config["AWS_ACCESS_KEY"],
        aws_secret_access_key=app.config["AWS_ACCESS_SECRET"],
    )

    def upload_file(data: dict) -> str:
        """
        Upload a file to AWS S3
        """
        try:
            data["stream"] = base64.b64decode(data["stream"])
            data["stream"] = io.BytesIO(data["stream"])
            file = FileStorage(**data)

            s3.upload_fileobj(
                file,
                app.config["S3_BUCKET_NAME"],
                data["filename"],
                ExtraArgs={
                    "ContentType": data["content_type"],
                },
            )
            return f"{app.config['S3_BUCKET_BASE_URL']}/{data['filename']}"
        except Exception:
            raise UploadFailedException()

    return upload_file


def renaming_file(filename: str):
    uploaded_date = datetime.utcnow()

    if filename is None:
        raise BadRequestException(INVALID_FILENAME)

    splitted = filename.rsplit(".", 1)
    if len(splitted) < 2:
        raise BadRequestException(INVALID_FILENAME)

    updated_filename = splitted[0]
    file_extension = splitted[1]
    updated_filename = secure_filename(updated_filename.lower())
    updated_filename = f"{uploaded_date.strftime('%Y%m%d%H%M%S')}--{updated_filename}"
    updated_filename = f"{updated_filename}.{file_extension}"

    return updated_filename
