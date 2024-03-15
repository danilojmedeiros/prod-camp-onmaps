import os

"""
    Variaveis booleanas e objetos nao poderao ser definidas nas variaveis de ambiente,
    pois todas serao convertidas para string.
    Para as variaveis definidas com "os.environ.get()" o primeiro valor é referente
    a variavel que está buscando, o segundo valor será usado como valor padrão caso
    não encontre nas variaveis de ambiente.
"""
API_NAME = "Servico API"
VERSION_API = '1.0.1'
TITLE_API = "api-onmaps"
DESCRIPTION_API = "API."

# Flask settings
FLASK_SERVER_NAME = None
FLASK_HOST = os.environ.get('FLASK_HOST', "0.0.0.0")
FLASK_PORT = os.environ.get('FLASK_PORT', "5000")
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

URL_PREFIX = os.environ.get('URL_PREFIX', '')

PATH_LOG = os.environ.get("PATH_LOG", "./log_project_name")
POOL_CPU = int(os.environ.get("POOL_CPU", os.cpu_count()-1))
