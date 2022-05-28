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
    from app.handlers.auth import AuthHandler

    register_shell_context("User", User)

    # Configuring auth
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    auth_controller = AuthController(auth_service)
    auth_handler = AuthHandler(auth_controller)
    app.register_blueprint(auth_handler.blueprint, url_prefix="/auth")


def configure_user(app: Flask, db: SQLAlchemy):
    from app.repositories.user import UserRepository
    from app.services.user import UserService
    from app.controllers.user import UserController
    from app.handlers.user import UserHandler

    # Configuring auth
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    user_controller = UserController(user_service)
    user_handler = UserHandler(user_controller)
    app.register_blueprint(user_handler.blueprint, url_prefix="/user")


def configure_song(app: Flask, db: SQLAlchemy):
    from app.models.song import Song
    from app.repositories.song import SongRepository
    from app.services.song import SongService
    from app.controllers.song import SongController
    from app.handlers.song import SongHandler
    from app.common.file import create_file_uploader

    register_shell_context("Song", Song)
    upload_file = create_file_uploader(app)

    # Configuring song
    song_repository = SongRepository(db)
    song_service = SongService(app, song_repository, upload_file)
    song_controller = SongController(song_service)
    song_handler = SongHandler(song_controller)
    app.register_blueprint(song_handler.blueprint, url_prefix="/song")


def configure_playlist(app: Flask, db: SQLAlchemy):
    from app.models.playlist import Playlist
    from app.repositories.playlist import PlaylistRepository
    from app.repositories.song import SongRepository
    from app.services.playlist import PlaylistService
    from app.controllers.playlist import PlaylistController
    from app.handlers.playlist import PlaylistHandler

    register_shell_context("Playlist", Playlist)

    # Configuring playlist
    playlist_repository = PlaylistRepository(db)
    song_repository = SongRepository(db)
    playlist_service = PlaylistService(playlist_repository, song_repository)
    playlist_controller = PlaylistController(playlist_service)
    playlist_handler = PlaylistHandler(playlist_controller)
    app.register_blueprint(playlist_handler.blueprint, url_prefix="/playlist")


def create_app(environment="development"):
    app = Flask(__name__)
    app.config.from_object(configurations[environment])
    configurations[environment].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    configure_auth(app, db)
    configure_user(app, db)
    configure_song(app, db)
    configure_playlist(app, db)

    @app.errorhandler(404)
    def resource_not_found():
        return jsonify({"error": "Resource not found"})

    @app.errorhandler(500)
    def internal_server_error():
        return jsonify({"error": "Internal server error"})

    @app.shell_context_processor
    def make_shell_context():
        register_shell_context("db", db)
        return shell_context

    return app
