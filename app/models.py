from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# UserMixin => traz métodos úteis para a classe User funcionar 
# com Flask-Login (como autenticação, controle de sessão).

# User -> usuários do sistema, para login e controle de acesso
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # criando relação entre o usuario e os seus registros de medicação
    # lazy=True => registros carregados quando acessados
    registers = db.relationship('Register', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.name}>'
    
class Medication(db.Model):
    __tablename__ = 'medications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    dosage = db.Column(db.String(50)) # Ex.: '500mg' ou '2 comprimidos'
    hour = db.Column(db.String(50))
    stock = db.Column(db.Integer, default=0)

    registers = db.relationship('Register', backref='medication', lazy=True)

    def __repr__(self):
        return f'<Medicamento {self.name}>'

class Register(db.Model):
    __tablename__ = 'registers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable=False)
    date_time = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    dosage = db.Column(db.String(50))
    observation = db.Column(db.Text)

    def __repr__(self):
        return f'<Registro {self.id} - User {self.user_id} - Medicamento {self.medication_id}>'
