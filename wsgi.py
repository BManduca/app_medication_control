import logging
# usado no Docker/gunicorn para rodar app em prod
from app import create_app

app = create_app()

# logs informativos => painel do Render
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
