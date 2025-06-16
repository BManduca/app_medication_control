import os
from flask import Blueprint
from flask_migrate import upgrade

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/run-migrations")
def run_migrations():
    if os.getenv("FLASK_ENV") == "production":
        try:
            upgrade()
            return "✅ Migrações aplicadas com sucesso!"
        except Exception as e:
            return f"❌ Erro ao aplicar as migrações: {str(e)}"
    return "⚠️ Esta rota só pode ser usada em produção."
