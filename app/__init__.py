import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import DevConfig, ProdConfig

load_dotenv()

# criando instancias "vazias" para o banco de dados, migração e autenticação
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Redirecionamento se não estiver logado
login_manager.login_message_category = 'info'

# função é responsável por criar e configurar a aplicação Flask, com banco de dados, 
# autenticação, rotas e configurações gerais
def create_app():
    app = Flask(__name__)

    # carregando configurações do arquivo config.py | define se é dev ou prod
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)

    # Inicializa extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # carrega dos modelos definidos em app/models.py no momento em que o app é criado
    from app import models

    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.main_routes import main

    app.register_blueprint(auth_bp) # Rotas de autenticação
    app.register_blueprint(dashboard_bp) # Rota protegia: /dashboard
    app.register_blueprint(main) # Rota principal: /

    return app

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
