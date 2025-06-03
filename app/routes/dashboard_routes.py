from datetime import datetime, timedelta
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import or_

from app.models import Medication, Register

dashboard_bp = Blueprint('user_dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Contagem
    total_medications = Medication.query.filter_by(user_id=current_user.id).count()
    total_registers = Register.query.filter_by(user_id=current_user.id).count()

    # Últimos registros
    recent_registers = (
        Register.query.filter_by(user_id=current_user.id)
        .order_by(Register.date_time.desc())
        .limit(5)
        .all()
    )

    # lembretes
    now = datetime.now().time()
    in_one_hour = (datetime.now() + timedelta(hours=1)).time()

    if now < in_one_hour:
        # faixa simples => 10:00 até 11:00
        reminders = Medication.query.filter(
            Medication.user_id == current_user.id,
            Medication.hour >= now,
            Medication.hour <= in_one_hour
        ).all()
    else:
        # faixa passa da 00:00 => 23:30 até 00:30
        reminders = Medication.query.filter(
            Medication.user_id == current_user.id,
            or_(
                Medication.hour >= now,
                Medication.hour <= in_one_hour
            )
        ).all()
    
    return render_template(
        'dashboard.html',
        user=current_user.name,
        total_medications=total_medications,
        total_registers=total_registers,
        recent_registers=recent_registers,
        reminders=reminders
    )
