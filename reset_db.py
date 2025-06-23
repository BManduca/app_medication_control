# reset_db.py
from app import create_app, db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ Banco de dados zerado e recriado com sucesso.")
