import os
from dotenv import load_dotenv

# evidenciando qual arquivo .env vai ser carregado: .env.dev(padrão) ou .env.prod
env_file = os.getenv("ENV_FILE", ".env.dev")
# carregando as variáveis do arquivo .env
load_dotenv(env_file)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY não está definida no ambiente!")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv("FLASK_ENV", "development")

    # Google OAuth 2.0
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///medications.db')

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
