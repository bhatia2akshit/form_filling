from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes import api


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    config_class.init_app(app)

    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(api, url_prefix="/api")

    return app
