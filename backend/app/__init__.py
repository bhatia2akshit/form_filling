from flask import Flask
from flask_cors import CORS
from app.routes import api
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def create_app():
    app = Flask(__name__)

    # Set up logging
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, "app.log"), maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Application startup")

    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(api, url_prefix="/api")

    return app
