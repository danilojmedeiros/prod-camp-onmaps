import logging.config
import os
from loguru import logger
from flask import Flask, Blueprint
from flask_cors import CORS

from service import settings
from service.restplus import api

# endpoints
from service.controller.start_controller import start as operation_basic_start
from service.controller.main_controller import pa as operation_basic_padroes

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
logger.add(settings.PATH_LOG, rotation="1 week")


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    CORS(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix=settings.URL_PREFIX)
    api.init_app(blueprint)

    api.add_namespace(operation_basic_start)
    api.add_namespace(operation_basic_padroes)
    flask_app.register_blueprint(blueprint)


def main(app):
    initialize_app(app)
    CORS(app)
    logger.debug("[+] --- starting at: {}:{}{}".format(settings.FLASK_HOST, settings.FLASK_PORT, settings.URL_PREFIX))
    return app


app = main(app)
