from flask import Flask
from app.controllers.routes.form_route import form_route
from app.controllers.routes.admin_route import admin_route
from dotenv import load_dotenv
import os 

load_dotenv()

def create_app():

    app = Flask(__name__)

    app.register_blueprint(form_route)
    app.register_blueprint(admin_route)

    app.secret_key = os.getenv("SECRET_KEY")

    return app