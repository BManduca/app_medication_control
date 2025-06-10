from datetime import time, date
from flask import abort
from werkzeug.security import generate_password_hash
import pytest
from app.models import Medication, User
from app import db

# TESTE DE VERIFICAÇÃO DE FALHAS, ERROS E SEGURANÇA

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

def test_dashboard_requires_login(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'login' in html.lower() or 'bem-vindo' in html.lower()

def test_edit_medication_of_other_user(client, app, logged_in_user):
    with app.app_context():
        # criando outro usuário e um novo medicamento para este mesmo
        other_user = User(
            name='Other User',
            email='other@example.com',
            password_hash=generate_password_hash('otherpass')
        )

        db.session.add(other_user)
        db.session.commit()

        medication = Medication(
            user_id=other_user.id,
            name='Novo medicamento do outro usuário',
            description='description no novo medicamento',
            dosage='500mg',
            expiration_date=date(2025, 12, 31),
            frequency='1x ao dia',
            hour=time(8, 0),
            stock=10,
            instructions='Instruções'
        )

        db.session.add(medication)
        db.session.commit()

        # logged_in_user tenta editar o medicamento do other_user
        response = client.post(f'/medications/edit/{medication.id}', data={
            'name': 'Nome novo medicamento',
            'description': 'description no novo medicamento',
            'dosage': '500mg',
            'frequency': '1x ao dia',
            'expiration_date': '31/12/2025',
            'hour': '08:00',
            'stock': 10,
            'instructions': 'Instruções'
        }, follow_redirects=True)

        # verificando se o usuário tem autorização
        assert response.status_code == 403
        html = response.data.decode('utf-8')
        assert 'não tem permissão' in html.lower() or '403' in html

def test_delete_medication_of_other_user(client, app, logged_in_user):
    with app.app_context():
        # criando outro usuário e um novo medicamento para este mesmo
        other_user = User(
            name='Other User',
            email='other@example.com',
            password_hash=generate_password_hash('otherpass')
        )

        db.session.add(other_user)
        db.session.commit()

        medication = Medication(
            user_id=other_user.id,
            name='Novo medicamento do outro novo usuário',
            description='description no novo medicamento do outro novo usuário',
            dosage='400mg',
            expiration_date=date(2025, 12, 31),
            frequency='1x ao dia',
            hour=time(10, 0),
            stock=15,
            instructions='Novas Instruções'
        )
        db.session.add(medication)
        db.session.commit()

        # logged_in_user tenta deletar o medicamento do other_user
        response = client.post(f'/medications/delete/{medication.id}', follow_redirects=True)

        assert response.status_code == 403
        html = response.data.decode('utf-8')
        assert 'não tem permissão' in html.lower() or '403' in html

@pytest.mark.parametrize('url, method', [
    ('/medications/add', 'GET'),
    ('/medications/edit/1', 'GET'), #id genérico, mas o teste espera o redirecionamento para tela de login
    ('/medications/delete/1', 'POST')
])
def test_protected_routes_require_login(client, url, method):
    if method == 'GET':
        response = client.get(url, follow_redirects=True)
    else:
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'login' in html.lower() or 'bem-vindo' in html.lower()

def test_error_403_page(client, app):
    with app.app_context():
        # criando rota fake, para forçar status_code 403
        @app.route('/force-route-403')
        def force_route_403():
            abort(403)
    
    response = client.get('/force-route-403')
    assert response.status_code == 403
    html = response.data.decode('utf-8')
    assert '403' in html or 'não tem permissão' in html.lower()

def test_error_404_page(client):
    response = client.get('/rota-inexistente')
    assert response.status_code == 404
    html = response.data.decode('utf-8')
    assert '404' in html or 'não foi encontrada' in html.lower()

def test_error_500_page(client, app):
    # EVITA QUE O FLASK PROPAGUE A EXCEÇÃO REAL NO TESTE.
    app.config["PROPAGATE_EXCEPTIONS"] = False

    with app.app_context():
        # criando rota fake para forçar status_code 500
        @app.route('/force-route-500')
        def force_route_500():
            raise Exception('Erro interno de teste.')

        response = client.get('/force-route-500')
        assert response.status_code == 500
        html = response.data.decode('utf-8')
        assert 'Erro interno' in html or 'internal server error' in html.lower()
