from flask import Flask, jsonify, cli
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.configs.config import configurations

db = SQLAlchemy()
migrate = Migrate()
shell_context = {}


def register_shell_context(name, obj):
    shell_context[name] = obj


def configure_auth(app: Flask, db: SQLAlchemy):
    from app.models.user import User
    from app.repositories.auth import AuthRepository
    from app.services.auth import AuthService
    from app.controllers.auth import AuthController
    from app.handlers.auth import create_auth_handlers

    register_shell_context("User", User)

    # Configuring auth
    auth_repository = AuthRepository(db)
    auth_service = AuthService(auth_repository)
    auth_controller = AuthController(auth_service)
    auth_handlers = create_auth_handlers(auth_controller)
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

    @app.shell_context_processor
    def make_shell_context():
        register_shell_context("db", db)
        return shell_context

    return app
