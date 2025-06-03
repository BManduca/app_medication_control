from werkzeug.security import generate_password_hash
from app.models import User
from app import db


def test_register_page(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b"Registrar" in response.data

def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_logout_redirect(client):
    response = client.get('/auth/logout', follow_redirects=True)
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
    assert 'senha inválidos' in html or 'senha incorreta' in html

def test_dashboard_requires_login(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200

    # aguarda ser redirecionado para o login
    assert b'Login' in response.data or b'Bem-vindo' in response.data
