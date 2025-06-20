import pytest
from app import create_app, db
from app.models import User, Medication
from config import TestConfig

# “fixture” — uma base reutilizável que pode ser passada para os testes
@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
