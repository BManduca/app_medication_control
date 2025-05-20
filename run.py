from flask_migrate import Migrate
from app import create_app, db

# chamada da função create_app e retorna uma instancia
# da aplicação Flask já configurada
app = create_app()
# garante que o Flask CLI reconheça os comandos flask db.
migrate = Migrate(app, db)

if __name__ == '__main__':
    # iniciar servidor desenvolvimento Flask
    app.run(debug=True)
