from flask import Flask, jsonify, cli
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.configs.config import configurations

db = SQLAlchemy()
migrate = Migrate()
shell_context = {}


def register_shell_context(name: str, obj: object):
    shell_context[name] = obj


def configure_auth(app: Flask, db: SQLAlchemy):
    from app.models.user import User
    from app.repositories.user import UserRepository
    from app.services.auth import AuthService
    from app.controllers.auth import AuthController
    from app.handlers.auth import create_auth_handlers

    register_shell_context("User", User)

    # Configuring auth
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    auth_controller = AuthController(auth_service)
    auth_handlers = create_auth_handlers(auth_controller)
    app.register_blueprint(auth_handlers, url_prefix="/auth")


def configure_user(app: Flask, db: SQLAlchemy):
    from app.repositories.user import UserRepository
    from app.services.user import UserService
    from app.controllers.user import UserController
    from app.handlers.user import create_user_handlers

    # Configuring auth
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    user_controller = UserController(user_service)
    user_handlers = create_user_handlers(user_controller)
    app.register_blueprint(user_handlers, url_prefix="/user")


def configure_song(app: Flask, db: SQLAlchemy):
    from app.models.song import Song

    register_shell_context("Song", Song)


def create_app(environment="development"):
    app = Flask(__name__)
    app.config.from_object(configurations[environment])
    configurations[environment].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    configure_auth(app, db)
    configure_user(app, db)
    configure_song(app, db)

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({"error": "Resource not found"})

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"error": "Internal server error"})

    @app.shell_context_processor
    def make_shell_context():
        register_shell_context("db", db)
        return shell_context

    return app
