from flask import Flask
from app.controllers.routes.form_route import form_route


def create_app():

    app = Flask(__name__)

    app.register_blueprint(form_route)

    return app