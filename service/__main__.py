from service.app import app
from service import settings


def start():
    app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, debug=settings.FLASK_DEBUG)
    print(__package__, ' started.')


if __name__ == '__main__':
    start()
