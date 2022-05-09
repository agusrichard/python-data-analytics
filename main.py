from flask import Flask

from repositories.auth import AuthRepository
from services.auth import AuthService
from handlers.auth import init_auth_handlers

app = Flask(__name__)

# Configuring auth
auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)
auth_handlers = init_auth_handlers(auth_service)
app.register_blueprint(auth_handlers, url_prefix="/auth")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
