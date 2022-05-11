from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.configs.config import configurations

db = SQLAlchemy()
migrate = Migrate()


def configure_auth(app: Flask, db: SQLAlchemy):
    from app.models.user import User
    from app.repositories.auth import AuthRepository
    from app.services.auth import AuthService
    from app.handlers.auth import init_auth_handlers

    # Configuring auth
    auth_repository = AuthRepository(db, User)
    auth_service = AuthService(auth_repository)
    auth_handlers = init_auth_handlers(auth_service)
    app.register_blueprint(auth_handlers, url_prefix="/auth")


def create_app(environment="development"):
    app = Flask(__name__)
    app.config.from_object(configurations[environment])
    configurations[environment].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    configure_auth(app, db)

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({"error": "Resource not found"})

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"error": "Internal server error"})

    return app
