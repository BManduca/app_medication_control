from datetime import date, time
import pytest
from app.models import Medication, User, MedicationReminder
from app import db

# utilitário para realização de login
def login(client, email, password):
    return client.post('/auth/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)

# criando usuário para testes
@pytest.fixture
def user_and_medication(app):
    with app.app_context():
        user = User(name='Reminder tester', email='reminder@example.com')
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

        medication = Medication(
            name='Dipirona',
            description='Descrição teste',
            dosage='500mg',
            expiration_date=date(2025, 12, 31),
            stock=5,
            user_id=user.id
        )
        db.session.add(medication)
        db.session.commit()
        return user.id, user.email, medication.id

def test_create_remidner(client, app, user_and_medication):
    user_id, user_email, medication_id = user_and_medication
    login(client, user_email, '123456')

    response = client.post('/reminders/add', data={
        'medication_id': medication_id,
        'time': '08:00',
        'frequency': 'daily',
        'active': True
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'Lembrete criado com sucesso' in html

    with app.app_context():
        reminder = MedicationReminder.query.filter_by(user_id=user_id).first()
        assert reminder is not None
        assert reminder.medication_id == medication_id
        assert reminder.time == time(8, 0)

def test_edit_reminder(client, app, user_and_medication):
    with app.app_context():
        user_id, user_email, medication_id = user_and_medication
        reminder = MedicationReminder(
            user_id=user_id,
            medication_id=medication_id,
            time=time(9, 0),
            frequency='once',
            active=True
        )
        db.session.add(reminder)
        db.session.commit()
        reminder_id = reminder.id

    login(client, user_email, '123456')
    response = client.post(f'/reminders/{reminder_id}/edit', data={
        'medication_id': medication_id,
        'time': '10:00',
        'frequency': 'weekly'
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'Lembrete atualizado com sucesso' in html

    with app.app_context():
        updated = db.session.get(MedicationReminder, reminder_id)
        assert updated.time == time(10, 0)
        assert updated.frequency == 'weekly'
        assert updated.active is False

def test_delete_reminder(client, app, user_and_medication):
    with app.app_context():
        user_id, user_email, medication_id = user_and_medication
        reminder = MedicationReminder(
            user_id=user_id,
            medication_id=medication_id,
            time=time(11, 0),
            frequency='once',
            active=True
        )
        db.session.add(reminder)
        db.session.commit()
        reminder_id = reminder.id

    login(client, user_email, '123456')
    response = client.post(f'/reminders/{reminder_id}/delete', follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'Lembrete excluído com sucesso' in html

    with app.app_context():
        deleted = db.session.get(MedicationReminder, reminder_id)
        assert deleted is None

def test_reminder_visibility(client, app, user_and_medication):
    user_id, user_email, medication_id = user_and_medication
    with app.app_context():
        other_user = User(name='Outro', email='outro@example.com')
        other_user.set_password('othersenha')
        db.session.add(other_user)
        db.session.commit()

        other_med = Medication(
            name='OutroMed',
            description='Outra descrição',
            dosage='100mg',
            expiration_date=date(2025, 8, 31),
            stock=2,
            user_id=other_user.id
        )
        db.session.add(other_med)
        db.session.commit()

        other_reminder = MedicationReminder(
            user_id=other_user.id,
            medication_id=other_med.id,
            time=time(14, 0),
            frequency='once',
            active=True
        )
        db.session.add(other_reminder)
        db.session.commit()

    login(client, user_email, '123456')
    response = client.get('/medications/reminders')
    html = response.data.decode('utf-8')
    assert 'OutroMed' not in html
