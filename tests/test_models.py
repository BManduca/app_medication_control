from datetime import date
from app import db
from app.models import User, Medication, Register

# teste criação de usuário e senha segura
def teste_creste_user(app):
    with app.app_context():
        user = User(name="Test User", email="test@example.com")
        user.set_password("12345")

        db.session.add(user)
        db.session.commit()

        saved_user = db.session.get(User, user.id)
        assert saved_user is not None
        assert saved_user.name == "Test User"
        assert saved_user.email == "test@example.com"
        assert saved_user.password_hash != "12345"
        assert saved_user.check_password("12345")
        assert not saved_user.check_password("wrong")

        # testa representação textual opcional
        assert repr(saved_user) == f'<User {saved_user.name}>'

def test_create_medication(app):
    with app.app_context():
        user = User(name="Med User", email="med@example.com")
        user.set_password("12345")

        db.session.add(user)
        db.session.commit()

        med = Medication(
            user=user,
            name="Paracetamol",
            description="Medicamento para dor",
            dosage="500mg",
            expiration_date = date(2025, 12, 31),
            frequency="2x ao dia",
            stock=10,
            instructions="Tomar após o café e a janta"
        )

        db.session.add(med)
        db.session.commit()
        
        saved_med = db.session.get(Medication, med.id)
        assert saved_med is not None
        assert saved_med.name == "Paracetamol"
        assert saved_med.description == "Medicamento para dor"
        assert saved_med.dosage == "500mg"
        assert saved_med.expiration_date == date(2025, 12, 31)
        assert saved_med.frequency == "2x ao dia"
        assert saved_med.stock == 10.0 # confirmado como float
        assert saved_med.instructions == "Tomar após o café e a janta"
        assert saved_med.user_id == user.id

# teste criação de registro de uso do medicamento
def test_create_register(app):
    with app.app_context():
        user = User(name="Reg User", email="reg@example.com")
        user.set_password("12345")

        db.session.add(user)
        db.session.commit()

        med=Medication(
            user=user,
            name="Ibuprofeno",
            description="Anti-inflamatório",
            dosage="200mg",
            expiration_date = date(2025, 12, 31),
            stock=20
        )
        
        db.session.add(med)
        db.session.commit()

        reg = Register(
            user_id=user.id,
            medication_id=med.id,
            amount_administered="1 comprimido",
            observation="Sem efeitos adversos"
        )
        db.session.add(reg)
        db.session.commit()

        saved_reg = db.session.get(Register, reg.id)
        assert saved_reg is not None
        assert saved_reg.amount_administered == "1 comprimido"
        assert saved_reg.observation == "Sem efeitos adversos"
        assert saved_reg.user_id == user.id
        assert saved_reg.medication_id == med.id

def test_user_deletation_cascades_medications(app):
    with app.app_context():
        user = User(name="Del user", email="del@example.com")
        user.set_password("12345")

        db.session.add(user)
        db.session.commit()

        med = Medication(
            user=user,
            name='Aspirine',
            description='Analgésico e antipirético',
            dosage='100mg',
            expiration_date=date(2025, 12, 31),
            stock=5
        )

        db.session.add(med)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        assert db.session.query(User).count() == 0
        # se houver cascade configurado
        assert db.session.query(Medication).count() == 0
