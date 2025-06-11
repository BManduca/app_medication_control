from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

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
        
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page and not is_safe_url(next_page):
                return abort(400)
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page or url_for('user_dashboard.dashboard'))
        else:
            flash('E-mail ou senha inválidos! Tente novamente.', 'danger')
        
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Você efetuou logout da sua conta!', 'info')
    return redirect(url_for('auth.login'))
