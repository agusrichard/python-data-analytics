import boto3
from flask import Flask
from typing import Callable
from werkzeug.datastructures import FileStorage


def create_file_uploader(app: Flask) -> Callable:
    """
    Create a file uploader
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=app.config["AWS_ACCESS_KEY"],
        aws_secret_access_key=app.config["AWS_ACCESS_SECRET"],
    )

    def upload_file(file: FileStorage) -> str:
        """
        Upload a file to AWS S3
        """
        try:
            s3.upload_fileobj(
                file,
                app.config["S3_BUCKET_NAME"],
                file.filename,
                ExtraArgs={
                    "ContentType": file.content_type,
                },
            )
            return f"{app.config['S3_BUCKET_BASE_URL']}/{file.filename}"
        except Exception as e:
            print("An error occurred uploading file to S3", str(e))

    return upload_file
