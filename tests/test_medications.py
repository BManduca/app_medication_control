from werkzeug.security import generate_password_hash
from app.models import Medication, User
from app import db

# TESTE DE VALIDAÇÕES DAS FUNCIONALIDADES DOS MEDICAMENTOS

def create_test_user(app):
    # cria um usuário de teste no banco, para teste em rotas protegidas
    with app.app_context():
        user = User(
            name="Test User",
            email="test@example.com",
            password_hash=generate_password_hash("testpassword")
        )
        db.session.add(user)
        db.session.commit()
        return user
    
def login(client):
    # realizar login do usuário test
    return client.post("/auth/login", data={
        'email': 'test@example.com',
        'password': 'testpassword'
    }, follow_redirects=True)

def test_medications_list_page(client, app):
    create_test_user(app)
    login(client)

    response = client.get('/medications', follow_redirects=True)
    assert response.status_code == 200
    assert b"Medicamentos" in response.data or b"Lista" in response.data

def test_add_medication_page(client, app):
    create_test_user(app)
    login(client)

    response = client.get('/medications/add')
    assert response.status_code == 200
    assert b"Adicionar" in response.data

def test_add_medication(client, app):
    create_test_user(app)
    login(client)

    response = client.post('/medications/add', data={
        "name": "TesteMed",
        "description": "Medicamento para teste",
        "dosage": "500mg",
        "expiration_date": "25/09/2025",
        "frequency": "1x ao dia",
        "hour": "08:00",
        "stock": 10,
        "instructions": "Tomar após o café da manhã"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"TesteMed" in response.data

    with app.app_context():
        # confirmando no banco
        medication = Medication.query.filter_by(name="TesteMed").first()
        assert medication is not None
        assert medication.dosage=="500mg"
