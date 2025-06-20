from datetime import datetime, timezone
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import DevConfig, ProdConfig

# criando instancias "vazias" para o banco de dados, migração e autenticação
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Redirecionamento se não estiver logado
login_manager.login_message = 'Você precisa estar logado para acessar esta página!'
login_manager.login_message_category = 'warning' # categoria do flash

# função é responsável por criar e configurar a aplicação Flask, com banco de dados, 
# autenticação, rotas e configurações gerais
def create_app(testing=False, config_class=None):
    app = Flask(__name__)

    # caso o config_class seja passado explicitamente
    if config_class:
        app.config.from_object(config_class)

    # Se Testing=Tre, configuração inline para testes (mínimas)
    elif testing:
        app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,  # Desativa CSRF para testes
            "GOOGLE_CLIENT_ID": "fake-client-id",
            "GOOGLE_CLIENT_SECRET": "fake-client-secret"
        })
    # Configuração baseada no ambiente (dev/prod)
    else:
        # carregando configurações do arquivo config.py
        env = os.getenv('FLASK_ENV', 'development')
        if env == 'production':
            app.config.from_object(ProdConfig)
        else:
            app.config.from_object(DevConfig)

    # Inicializa extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes.auth_routes import auth_bp, init_oauth
    init_oauth(app)

    # carrega dos modelos definidos em app/models.py no momento em que o app é criado
    from app import models

    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.medication_routes import medication_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.main_routes import main

    app.register_blueprint(auth_bp) # Rotas de autenticação
    app.register_blueprint(dashboard_bp) # Rota protegia: /dashboard
    app.register_blueprint(medication_bp) # Rotas dos medicamentos
    app.register_blueprint(main) # Rota principal: /
    app.register_blueprint(admin_bp) # Registrando rota de Migração: /run-migrations

    @app.context_processor
    def inject_now():
        return {'now': datetime.now(timezone.utc)}
    
    from .error_handlers import init_error_handlers
    # inicializando handlers de erro
    init_error_handlers(app)

    return app

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
