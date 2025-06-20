from unittest.mock import patch
import pytest
from flask import url_for
from app.models import User
from app import db

def test_google_login_redirect(client):
    response = client.get('/auth/login/google')
    # verificando se redireciona para o Google OAuth
    assert response.status_code == 302
    assert 'accounts.google.com' in response.location or 'google.com' in response.location

@patch('app.routes.auth_routes.oauth.google.authorize_access_token')
@patch('app.routes.auth_routes.oauth.google.get')
def test_google_authorize_new_user(mock_get, mock_authorize_token, client, app):
    # simulando o token e dados do google
    mock_authorize_token.return_valeu = {'access_token': 'fake-token'}
    mock_get.return_value.json.return_value = {
        'email': 'newgoogleuser@example.com',
        'name': 'Google User'
    }

    with app.app_context():
        response = client.get('/auth/login/google/authorized', follow_redirects=True)

        # Verificando se o usuário foi criado e logado com sucesso
        user = User.query.filter_by(email='newgoogleuser@example.com').first()

        assert user is not None
        assert user.is_google_user is True
        html = response.data.decode('utf-8')
        assert 'Bem-vindo' in html

@patch('app.routes.auth_routes.oauth.google.authorize_access_token')
@patch('app.routes.auth_routes.oauth.google.get')
def test_google_authorize_existing_email_with_password(mock_get, mock_authorize_token, client, app):
    # Usuário já registrado com senha via cadastro tradicional
    with app.app_context():
        user = User(name='Local User', email='existing@example.com')
        user.set_password('senha123')
        db.session.add(user)
        db.session.commit()

    # simulando Google retornando o mesmo email
    mock_authorize_token.return_value = {'access_token': 'fake-token'}
    mock_get.return_value.json.return_value = {
        'email': 'existing@example.com',
        'name': 'Google User'
    }

    response = client.get('/auth/login/google/authorized', follow_redirects=True)
    html = response.data.decode('utf-8')
    assert 'email já está registrado com senha' in html.lower()

@patch('app.routes.auth_routes.oauth.google.authorize_access_token', side_effect=Exception("Erro OAuth"))
def test_google_authorized_token_failure(mock_auth_token, client):
    response = client.get('/auth/login/google/authorized', follow_redirects=True)
    html = response.data.decode('utf-8')
    assert 'erro na autenticação com google' in html.lower()
