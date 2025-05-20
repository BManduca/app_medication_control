from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('As senhas informadas não coincidem.', 'danger')
            return redirect(url_for('auth.register'))
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Já existe um usuário registrado com esse e-mail!', 'warning')
            return redirect(url_for('auth.register'))
        
        new_user = User(name=name, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash(f'Cadastro do usuário {name} realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('user_dashboard.dashboard'))
        else:
            flash('E-mail ou senha inválidos!', 'danger')
            return redirect(url_for('auth.login'))
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você efetuou logout da sua conta!', 'info')
    return redirect(url_for('auth.login'))
