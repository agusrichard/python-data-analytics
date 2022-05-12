import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture
def app():
    from app import create_app

    app_ = create_app("testing")
    app_context = app_.app_context()
    app_context.push()

    yield app_

    app_context.pop()


@pytest.fixture
def db(app: Flask):
    from app import db

    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture
def client(app: Flask, db: SQLAlchemy):
    return app.test_client()
