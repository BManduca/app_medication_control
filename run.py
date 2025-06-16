import os
from flask_migrate import Migrate
from app import create_app, db

# chamada da função create_app e retorna uma instancia
# da aplicação Flask já configurada
app = create_app()
# garante que o Flask CLI reconheça os comandos flask db.
migrate = Migrate(app, db)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # iniciar servidor desenvolvimento Flask
    app.run(debug=True, host="0.0.0.0", port=port)
