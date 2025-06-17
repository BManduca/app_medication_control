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
    password_hash = db.Column(db.Text, nullable=True)  # agora permite NULL para usuários Google
    is_google_user = db.Column(db.Boolean, default=False) # <------- Flag

    registers = db.relationship('Register', backref='user', lazy=True)
    medications = db.relationship('Medication', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'
    
class Medication(db.Model):
    __tablename__ = 'medications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), name='fk_medications_user_id', nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    dosage = db.Column(db.String(50), nullable=False) # Ex.: '500mg' ou '2 comprimidos'
    expiration_date = db.Column(db.Date, nullable=False)
    frequency = db.Column(db.String(50), nullable=True) # Ex.: 3x ao dia
    hour = db.Column(db.Time, nullable=True)
    stock = db.Column(db.Float, default=0.0)
    cont_total_use_register = db.Column(db.Integer, default=0)
    instructions = db.Column(db.Text, nullable=True)  # pode ser texto longo e opcional

    registers = db.relationship('Register', backref='medication', lazy=True)

    # caso medicamento seja deletado, seus lembretes automaticamente também serão
    reminders = db.relationship(
        'MedicationReminder',
        back_populates='medication',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Medication {self.name}>'

class Register(db.Model):
    __tablename__ = 'registers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), name='fk_registers_medication_id', nullable=False)
    date_time = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    amount_administered = db.Column(db.String(50), nullable=True)
    observation = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Register {self.id} - User {self.user_id} - Medication {self.medication_id}>'
    
class MedicationReminder(db.Model):
    __tablename__ = 'medicationsreminders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), name='fk_medicationsreminders_medication_id', nullable=False)
    time = db.Column(db.Time, nullable=False) # horário do lembrete
    active = db.Column(db.Boolean, default=True) # se o lembrete está ativo ou não
    frequency = db.Column(db.String(20), default='once') # 'once', 'daily', 'weekly'
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='reminders', lazy=True)
    medication = db.relationship('Medication', back_populates='reminders', lazy=True)

    def __repr__(self):
        med_name = self.medication.name if self.medication else 'Unknown'
        return f'<ReminderID {self.id} - MedID {self.medication_id} - {med_name} at {self.time.strftime('%H:%M')}>'
