from datetime import time
from werkzeug.security import generate_password_hash
import pytest
from app.models import User
from app import db

# TESTES DE VALIDAÇÕES DE FOMULÁRIO DE MEDICAMENTOS

@pytest.fixture
def logged_in_user(client, app):
    with app.app_context():
        user = User(
            name='Validation User',
            email='validation@example.com',
            password_hash=generate_password_hash('validationpass')
        )

        db.session.add(user)
        db.session.commit()

    # efetuar login
    client.post('/auth/login', data={
        'email': 'validation@example.com',
        'password': 'validationpass'
    }, follow_redirects=True)

def test_add_medication_missing_required_fields(client, logged_in_user):
    response = client.post('medications/add', data = {
        "name": "",
        "description": "Medicamento para teste",
        "dosage": "",
        "frequency": "1x ao dia",
        "hour": "08:00",
        "stock": "",
        "instructions": "Tomar após o café da manhã"
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'Este campo é obrigatório' in html or 'required' in html

def test_add_medication_name_too_long(client, logged_in_user):
    long_name = 'A' * 200 # limite do name é 120
    response = client.post('/medications/add', data={
        'name': long_name,
        'description': 'Descrição teste',
        'dosage': '500mg',
        "expiration_date": "25/09/2025",
        'hour': '08:00',
        'stock': 5,
        'instructions': 'Instruções'
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode('utf-8')
    print(html)
    assert 'O nome deve ter no máximo 120 caracteres.' in html

def test_add_medication_negative_stock(client, logged_in_user):
    response = client.post('/medications/add', data={
        'name': 'TesteNegativo',
        'description': 'Descrição',
        'dosage': '500mg',
        "expiration_date": "25/09/2025",
        'stock': -10
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'O estoque não pode ser negativo.' in html or 'inválido' in html
