from flask_restplus import Api
from loguru import logger

from service import settings
from service.constants import codeHttp, mensagens
from service.responses.responses import ControllResponse

# Objeto para resposta
objResponse = ControllResponse()

api = Api(version=settings.VERSION_API, title=settings.TITLE_API,
          description=settings.DESCRIPTION_API, doc="/docs/")


@api.errorhandler
def default_error_handler(e):
    logger.exception(mensagens.ERROR_NOT_TREATMENT)

    if not settings.FLASK_DEBUG:
        return {'mensagem': mensagens.ERROR_NOT_TREATMENT}, codeHttp.ERROR_500
