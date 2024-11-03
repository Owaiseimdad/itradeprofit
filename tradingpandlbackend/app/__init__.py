# app/__init__.py

from flask import Flask
from flask_migrate import Migrate
from .models import db  # Import the db instance from models
from dotenv import load_dotenv
from .routes import register_routes
import os

def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # Set the SQLALCHEMY_DATABASE_URI from environment variable
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    register_routes(app)

    return app
