from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models import db

migrate = Migrate()


def configure_auth(app: Flask, db: SQLAlchemy):
    from models.user import User
    from repositories.auth import AuthRepository
    from services.auth import AuthService
    from handlers.auth import init_auth_handlers

    # Configuring auth
    auth_repository = AuthRepository(db, User)
    auth_service = AuthService(auth_repository)
    auth_handlers = init_auth_handlers(auth_service)
    app.register_blueprint(auth_handlers, url_prefix="/auth")


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    configure_auth(app, db)

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({"error": "Resource not found"})

    return app
