from werkzeug.security import generate_password_hash
from app.models import User
from app import db

# TESTES DE AUTENTICAÇÃO

def test_register_page(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b"Cadastrar" in response.data

def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_logout_redirect(client):
    response = client.post('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data or b"Bem-vindo" in response.data

def test_login_wrong_password(client, app):
    with app.app_context():
        user = User(
            name='Test User',
            email='testuser@example.com',
            password_hash=generate_password_hash('correctpassword')
        )

        db.session.add(user)
        db.session.commit()

    # efetuando logim com senha errada
    response = client.post('/auth/login', data={
        'email': 'testuser@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'senha não cadastrada ou incorreta' in html.lower()

def test_dashboard_requires_login(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200

    # aguarda ser redirecionado para o login
    assert b'Login' in response.data or b'Bem-vindo' in response.data

def test_register_user(client, app):
    response = client.post('/auth/register', data={
        'username': 'New User',
        'email': 'new@example.com',
        'password': '123456',
        'confirm_password': '123456'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email='new@example.com').first()
        assert user is not None
        assert user.name == 'New User'

def test_login_success(client, app):
    with app.app_context():
        user = User(name='Login Success', email='loginsuccess@example.com')
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

    response = client.post('/auth/login', data={
        'email': 'loginsuccess@example.com',
        'password': '123456'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Login' in response.data

def test_duplicate_email_register_fails(client, app):
    with app.app_context():
        user = User(name='Dup user', email='dup@example.com')
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

    response = client.post('/auth/register', data={
        'username': 'Another Dup',
        'email': 'dup@example.com',
        'password': '123456',
        'confirm_password': '123456'
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'Cadastrar' in html and 'Faça login ou use outro email' in html

def test_login_no_existent_user(client):
    response = client.post('/auth/login', data={
        'email': 'naoexiste@example.com',
        'password': 'senhateste'
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'e-mail não cadastrado ou inválido' in html.lower()

def test_register_empty_field(client):
    response = client.post('/auth/register', data={
        'username': '',
        'email': '',
        'password': '',
        'confirm_password': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'O nome de usuário é obrigatório' in html or 'O e-mail é obrigatório' in html
    assert 'A confirmação da senha é obrigatória' in html or 'Este campo é obrigatório' in html
