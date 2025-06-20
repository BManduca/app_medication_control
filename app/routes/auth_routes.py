from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, render_template, redirect, url_for, flash, request
from authlib.integrations.flask_client import OAuth
from flask_login import login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
oauth = OAuth()

# Função para inicializar OAuth com configuração do Google
def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Erro no campo {getattr(form, field).label.text}: {error}', 'danger')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data.lower()
        existing_user = User.query.filter_by(email=email).first()

        # verifica se já existe um usuário com o email utilizado
        if existing_user:
            flash('Este e-mail já foi registrado. Faça login ou use outro email!', 'danger')
            return redirect(url_for('auth.register'))

        # lógica para criar usuário e salvar no banco
        user = User(name=form.username.data, email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
    
        flash(f'Cadastro do usuário {user.name} realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    
    flash_form_errors(form)
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        if user:
            if user.is_google_user:
                flash('Este usuário foi cadastrado via Google. Por favor, faça login usando o Google.', 'warning')
                return redirect(url_for('auth.login'))
            elif user.check_password(form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                if next_page and not is_safe_url(next_page):
                    return abort(400)
                flash('Login realizado com sucesso!', 'success')
                return redirect(next_page or url_for('user_dashboard.dashboard'))
            else:
                flash('Senha não cadastrada ou incorreta! Tente novamente.', 'danger')
        else:
            flash('E-mail não cadastrado ou inválido! Tente novamente.', 'danger')
        
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Você efetuou logout da sua conta!', 'info')
    return redirect(url_for('auth.login'))

# ----------------------------
# GOOGLE OAUTH ROUTES
# ----------------------------

@auth_bp.route('/login/google')
def login_google():
    redirect_uri = url_for('auth.google_authorized', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/google/authorized')
def google_authorized():
    try:
        token = oauth.google.authorize_access_token()
    except Exception as e:
        flash('Erro na autenticação com Google: ' + str(e), 'danger')
        return redirect(url_for('auth.login'))

    if not token:
        flash('Autenticação com Google falhou!', 'danger')
        return redirect(url_for('auth.login'))
    
    # Obtendo user info diretamente do endpoint userinfo com o token de acesso
    try:
        resp = oauth.google.get('https://openidconnect.googleapis.com/v1/userinfo', token=token)
        user_info = resp.json()
    except Exception as e:
        flash('Erro ao obter informações do usuário Google: ' + str(e), 'danger')
        return redirect(url_for('auth.login'))

    email = user_info.get('email')
    name = user_info.get('name')

    if not email:
        flash('Não foi possível obter o email da conta Google.', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, is_google_user=True)
        db.session.add(user)
        db.session.commit()
    elif not user.is_google_user:
        flash('Este email já está registrado com senha. Use o login tradicional.', 'danger')
        return redirect(url_for('auth.login'))

    login_user(user)
    flash(f'Bem-vindo(a), {user.name} (login Google)!', 'success')
    return redirect(url_for('user_dashboard.dashboard'))
