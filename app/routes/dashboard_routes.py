from datetime import date, datetime, timedelta, timezone
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.utils import convert_utc_to_fuso_brasilia

from app.models import Medication, Register, MedicationReminder

dashboard_bp = Blueprint('user_dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():

    # Contagem de medicamentos ativos com estoque > 0
    medications_in_stock = Medication.query.filter_by(user_id=current_user.id, active=True).filter(Medication.stock > 0).count()

    # Total de registros de uso dos medicamentos
    total_registers = Register.query.join(Medication).filter(Medication.user_id==current_user.id).count()

    # Últimos registros de uso (os 5 mais recentes)
    recent_registers = (
        Register.query.join(Medication)
        .filter(Medication.user_id == current_user.id)
        .order_by(Register.date_time.desc())
        .limit(5)
        .all()
    )

    # lembretes para o horário atual e no intervalo de 1 hora
    now_utc = datetime.now(timezone.utc)
    now_time_brasilia = convert_utc_to_fuso_brasilia(now_utc)

    five_min_ago = (now_time_brasilia - timedelta(minutes=5)).time()
    five_min_later = (now_time_brasilia + timedelta(minutes=5)).time()

    # Lembretes ativos dentro do próximo intervalor de 1h
    if five_min_ago < five_min_later:
        reminders = MedicationReminder.query.join(Medication).filter(
            Medication.user_id == current_user.id,
            MedicationReminder.active == True,
            MedicationReminder.time >= five_min_ago,
            MedicationReminder.time <= five_min_later
        ).all()
    else:
        # Faixa de tempo atravessa a meia-noite (ex.: 23:30 até 00:30)
        reminders = MedicationReminder.query.join(Medication).filter(
            Medication.user_id == current_user.id,
            MedicationReminder.active == True,
            or_(
                MedicationReminder.time >= five_min_ago,
                MedicationReminder.time <= five_min_later
            )
        ).all()

    # medicamentos prestes a vencer próximos 30 dias (apenas ativos)
    due_date = date.today() + timedelta(days=30)
    expiring_medicines = Medication.query.filter(
        Medication.user_id == current_user.id,
        Medication.expiration_date.isnot(None),
        Medication.expiration_date <= due_date,
        Medication.expiration_date >= date.today(),
        Medication.active == True
    ).order_by(Medication.expiration_date).all()

    # Coletando todos os medicamentos do usuário para apresentar na seção 'Registrar uso'
    medications = Medication.query.filter_by(user_id=current_user.id, active=True).all()
    
    return render_template(
        'dashboard.html',
        user=current_user.name,
        medications_in_stock=medications_in_stock,
        total_registers=total_registers,
        recent_registers=recent_registers,
        reminders=reminders,
        expiring_medicines=expiring_medicines,
        medications=medications,
        current_date=date.today() # designado para o template calcular os dias restantes
    )
