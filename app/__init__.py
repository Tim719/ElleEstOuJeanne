import logging.config
from os import environ, path

from dotenv import load_dotenv
from flask import Flask

from .config import config as app_config


def create_app():
    # loading env vars from .env file
    load_dotenv()
    APPLICATION_ENV = get_environment()
    logging.config.dictConfig(app_config[APPLICATION_ENV].LOGGING)
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])

    jeanne_file = app_config[APPLICATION_ENV].JEANNE_FILE

    if not path.isfile(jeanne_file):
        with open(jeanne_file, 'w'): pass

    from .core.views import core as core_blueprint
    app.register_blueprint(
        core_blueprint
    )

    return app


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
