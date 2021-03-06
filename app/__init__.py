import logging.config
from os import environ, path

from dotenv import load_dotenv
from flask import Flask

from flask_mongoengine import MongoEngine

from .config import config as app_config

db = MongoEngine()

def create_app():
    # loading env vars from .env file
    load_dotenv()
    APPLICATION_ENV = get_environment()
    logging.config.dictConfig(app_config[APPLICATION_ENV].LOGGING)
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])

    db.init_app(app)

    from .core.views import core as core_blueprint
    app.register_blueprint(
        core_blueprint
    )

    return app


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
