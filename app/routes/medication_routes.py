import csv
import io
from datetime import datetime, timezone, timedelta
from flask import Blueprint, abort, render_template, redirect, url_for, flash, request, Response, jsonify
from flask_login import login_required, current_user
import pytz
from app import db
from app.models import Medication, MedicationReminder, Register
from app.forms import EditRegisterForm, FilterDateForm, MedicationForm, NameFilterForm, RegisterUseMedicationForm, ReminderForm
from app.utils import convert_utc_to_fuso_brasilia

medication_bp = Blueprint('medication', __name__)

# função para converter formato 'YYYY-MM-DD' para 'DD/MM/YYYY'
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        return date_str

@medication_bp.route('/medications')
@login_required
def list_medications():
    form = NameFilterForm(request.args)
    page = request.args.get('page', 1, type=int)

    name_filter = form.name.data or ''
    query = Medication.query.filter_by(user_id=current_user.id)

    # Filtro por nome (case-insensitive)
    if name_filter:
        query = query.filter(Medication.name.ilike(f"%{name_filter}%"))

    # Medicamentos ativos
    active_query = query.filter(Medication.active.is_(True)).order_by(Medication.name.asc())
    active_medications = active_query.paginate(page=page, per_page=10)

    # Medicamentos inativos
    inactive_query = query.filter(Medication.active.is_(False)).order_by(Medication.name.asc())
    inactive_medications = inactive_query.paginate(page=page, per_page=10)

    return render_template(
        "medications/list.html",
        active_medications=active_medications,
        inactive_medications=inactive_medications,
        name_filter=name_filter,
        name_filter_form=form
    )


@medication_bp.route('/medications/add', methods=['GET', 'POST'])
@login_required
def add_medication():
    form = MedicationForm()
    if form.validate_on_submit():
        expiration_date = form.expiration_date.data if form.expiration_date.data else None

        medication = Medication(
            user_id=current_user.id,
            name = form.name.data,
            description = form.description.data,
            dosage = form.dosage.data,
            expiration_date = expiration_date,
            frequency = form.frequency.data,
            hour = form.hour.data,
            stock = form.stock.data,
            cont_total_use_register = 0,
            instructions = form.instructions.data
        )
        db.session.add(medication)
        db.session.commit()
        flash("Medicamento adicionado com sucesso!", "success")
        return redirect(url_for("medication.list_medications"))
    return render_template("medications/add.html", form=form, title='Adicionar Medicamento')

@medication_bp.route('/medications/edit/<int:med_id>', methods=['GET', 'POST'])
@login_required
def edit_medication(med_id):
    medication = Medication.query.get_or_404(med_id)

    # validando usuário logado
    if medication.user_id != current_user.id:
        abort(403)
        
    form = MedicationForm(obj=medication)

    if request.method == 'GET' and medication.expiration_date:
        # apresenta o objeto datetime.date diretamente
        form.expiration_date.data = medication.expiration_date

    if form.validate_on_submit():
        expiration_date = form.expiration_date.data if form.expiration_date.data else None
            
        # atualizando informações 
        medication.name = form.name.data
        medication.description = form.description.data
        medication.dosage = form.dosage.data
        medication.expiration_date = expiration_date
        medication.frequency = form.frequency.data
        medication.hour = form.hour.data
        medication.stock = form.stock.data
        medication.instructions = form.instructions.data

        db.session.commit()
        flash("Medicamento atualizado com sucesso!", "success")
        return redirect(url_for("medication.list_medications"))
    return render_template("medications/edit.html", form=form, title='Editar Medicamento', medication=medication)


@medication_bp.route("/medications/use", methods=['GET', 'POST'])
@login_required
def register_use():
    med_id = request.args.get('med_id', type=int)
    medication = Medication.query.get_or_404(med_id)

    # Verifica se o medicamento pertence ao usuário
    if medication.user_id != current_user.id:
        abort(403)
    
    form = RegisterUseMedicationForm()

    if form.validate_on_submit():
        quantity_used_str = form.quantity.data
        observation = form.observation.data

        if not quantity_used_str:
            flash('A quantidade deve ser informada e maior que zero.', 'danger')
            return redirect(url_for('medication.register_use', med_id=med_id))
        
        # Convertendo quantidade para float, permitindo vírgula ou ponto
        try:
            quantity_float = float(quantity_used_str.replace(',', '.'))
        except ValueError:
            flash('Quantidade inválida! Use apenas números.', 'danger')
            return redirect(url_for('medication.register_use', med_id=med_id))
        
        if quantity_float <= 0:
            flash('A quantidade deve ser maior que zero.', 'danger')
            return redirect(url_for('medication.register_use', med_id=med_id))
        
        # Verifica estoque disponível
        if medication.stock is None or medication.stock < quantity_float:
            flash('Estoque insuficiente para registrar a quantidade desejada.', 'danger')
            return redirect(url_for('medication.register_use', med_id=med_id))
        
        # Cria registro de uso
        register = Register(
            user_id=current_user.id,
            medication_id=med_id,
            amount_administered=str(quantity_float),  # salvo como string, poderia ser float se quiser
            observation=observation,
            date_time=datetime.now(timezone.utc)
        )

        # Atualiza estoque
        medication.stock -= quantity_float

        medication.cont_total_use_register = (medication.cont_total_use_register or 0) + 1

        db.session.add(register)
        db.session.commit()

        flash(f'Uso do medicamento "{medication.name}" registrado com sucesso!', 'success')
        return redirect(url_for('medication.list_medications'))
    
    return render_template(
        'medications/register_use_medication.html',
        form=form,
        medication=medication
    )

@medication_bp.route('/history')
@login_required
def view_history():
    form = FilterDateForm(request.args)

    start_date = form.start_date.data
    end_date = form.end_date.data
    medication_id = request.args.get('medication')
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'date_desc')
    page = request.args.get('page', 1, type=int)

    # validação de datas coerentes ou impedir datas invertidas
    if start_date and end_date and start_date > end_date:
        flash('A data final não pode ser anterior à data inicial.', 'error')
        return redirect(url_for('medication.view_history'))
    
    # busca medicamentos do usuário para exibir no filtro
    medications = Medication.query.filter_by(user_id=current_user.id).order_by(Medication.name).all()

    # query base: registros do usuário atual 
    query = Register.query.join(Medication).filter(Medication.user_id == current_user.id)

    # filtro por data
    if start_date:
        start_datetime = datetime.combine(start_date, datetime.min.time())
        start_datetime_bras = pytz.timezone('America/Sao_Paulo').localize(start_datetime)
        start_datetime_utc = start_datetime_bras.astimezone(pytz.utc)
        query = query.filter(Register.date_time >= start_datetime_utc)

    if end_date:
        end_datetime = datetime.combine(end_date, datetime.max.time())
        end_datetime_bras = pytz.timezone('America/Sao_Paulo').localize(end_datetime)
        end_datetime_utc = end_datetime_bras.astimezone(pytz.utc)
        query = query.filter(Register.date_time <= end_datetime_utc)

    # filtro por medicamento especifico
    if medication_id:
        query = query.filter(Register.medication_id == medication_id)

    # busca textual
    if search:
        search_like = f"%{search}%"
        query = query.filter(
            db.or_(
                Register.observation.ilike(search_like),
                Medication.name.ilike(search_like)
            )
        )

    # ordenação flexível
    if sort == 'date_asc':
        query = query.order_by(Register.date_time.asc())
    elif sort == 'date_desc':
        query = query.order_by(Register.date_time.desc())
    elif sort == 'medication_asc':
        query = query.order_by(Medication.name.asc())
    elif sort == 'medication_desc':
        query = query.order_by(Medication.name.desc())
    else:
        query = query.order_by(Register.date_time.desc())

    # ordenação e paginação
    pagination = query.order_by(Register.date_time.desc()).paginate(page=page, per_page=10, error_out=False)
    registers = pagination.items

    # conversão para horário de Brasília
    for reg in registers:
        reg.date_time_local = convert_utc_to_fuso_brasilia(reg.date_time)

    # conversão de data para o formato 'DD/MM/YYYY' somente para exibição em filtros
    start_date_str = start_date.strftime('%d/%m/%Y') if start_date else ''
    end_date_str = end_date.strftime('%d/%m/%Y') if end_date else ''

    return render_template(
        'medications/view_history.html',
        form=form,
        medications=medications,
        registers=registers,
        pagination=pagination,
        start_date=start_date_str,
        end_date=end_date_str,
        search=search,
        sort=sort,
        selected_medication=medication_id
    )

@medication_bp.route('/medications/export/csv')
@login_required
def export_history_csv():
    form = FilterDateForm(request.args)

    start_date = form.start_date.data
    end_date = form.end_date.data
    medication_id = request.args.get('medication')

    # validando: data final não pode ser anterior a data inicial
    if start_date and end_date and start_date > end_date:
        flash('A data final não pode ser anterior à data inicial.', 'danger')
        return redirect(url_for('medication.view_history'))
    
    # ajustando hora final para 23:59:59 do dia
    if end_date:
        end_date = datetime.combine(end_date, datetime.max.time())

    # query base: registros do usuário atual
    query = Register.query.join(Medication).filter(Register.user_id == current_user.id)

    if start_date:
        # filtrar todos os registros apartir da data(start_date)
        query = query.filter(Register.date_time >= start_date)

    if end_date:
        # filtrar todos os registros até a data(end_date)
        query = query.filter(Register.date_time <= end_date)
    
    if medication_id:
        query = query.filter(Register.date_time.desc()).all()

    registers = query.order_by(Register.date_time.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Data/Hora Registro',
        'Medicamento',
        'Descrição',
        'Dosagem',
        'Data de validade',
        'Frequência',
        'Horário de uso',
        'Estoque atual',
        'Observação',
        'Quantidade admnistrada',
        'Instruções'
    ])

    for reg in registers:
        med = reg.medication
        expiration_date_str = med.expiration_date.strftime('%d/%m/%Y') if med.expiration_date else ''

        # convertendo estoque para float e formatando com 2 casas decimais, se não for None
        stock_value = ''
        if med.stock is not None:
            try:
                stock_float = float(med.stock)
                stock_value = f"{stock_float:.2f}"
            except (ValueError, TypeError):
                stock_value = '' # se der erro na conversão

        writer.writerow([
            reg.date_time.strftime('%d/%m/%Y %H:%M'),
            med.name,
            med.description or '',
            med.dosage or '',
            expiration_date_str,
            med.frequency or '',
            med.hour or '',
            stock_value,
            med.instructions or '',
            reg.amount_administered or '',
            reg.observation or ''
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            "Content-Disposition": "attachment; filename=historico_medicamentos.csv"
        }
    )

@medication_bp.route('/medications/delete/<int:med_id>', methods=['POST'])
@login_required
def delete_medication(med_id):
    medication = Medication.query.get_or_404(med_id)

    # Verifica se o medicamento pertence ao usuário
    if medication.user_id != current_user.id:
        # renderizando para o template 403.html
        abort(403)

    db.session.delete(medication)
    db.session.commit()
    flash("Medicamento removido com sucesso!", "info")
    return redirect(url_for('medication.list_medications'))

@medication_bp.route('/medications/deactivate/<int:med_id>', methods=['POST'])
@login_required
def deactivate_medication(med_id):
    medication = Medication.query.get_or_404(med_id)

    # Verifica se o medicamento pertence ao usuário
    if medication.user_id != current_user.id:
        abort(403)

    medication.active = False
    db.session.commit()
    flash('Medicamento arquivado com sucesso!', 'success')
    return redirect(url_for('medication.list_medications'))

@medication_bp.route('/medications/activate/<int:med_id>', methods=['POST'])
@login_required
def activate_medication(med_id):
    medication = Medication.query.get_or_404(med_id)

    # Verifica se o medicamento pertence ao usuário
    if medication.user_id != current_user.id:
        abort(403)

    medication.active = True
    db.session.commit()
    flash('Medicamento reativado com sucesso!', 'success')
    return redirect(url_for('medication.list_medications'))

@medication_bp.route('/medications/inactive')
@login_required
def inactive_medication_list():
    form = NameFilterForm(request.args)
    page = request.args.get('page', 1, type=int)

    name_filter = form.name.data or ''

    # Filtro por nome (case-insensitive)
    if name_filter:
        query = query.filter(Medication.name.ilike(f"%{name_filter}%"))

    inactive_medications = Medication.query.filter_by(user_id=current_user.id, active=False).paginate(page=page, per_page=6)
    return render_template(
        'medications/inactive_list.html',
        inactive_medications=inactive_medications,
        name_filter=name_filter,
        name_filter_form=form
    )

@medication_bp.route('/recent-registers')
@login_required
def recent_registers():
    # form = FilterDateForm(request.args)
    page = request.args.get('page', 1, type=int)

    now_utc = datetime.now(timezone.utc)
    now_timezone_brasilia = convert_utc_to_fuso_brasilia(now_utc)

    # inicio e fim do dia em Brasília
    start_today_bras = now_timezone_brasilia.replace(hour=0, minute=0, second=0, microsecond=0)
    end_today_bras = now_timezone_brasilia.replace(hour=23, minute=59, second=59, microsecond=999999)

    # convertendo inicio e fim do dia para UTC
    start_day_utc = start_today_bras.astimezone(pytz.utc)
    end_day_utc = end_today_bras.astimezone(pytz.utc)

    # buscanso apenas registros do usuário e do dia atual
    recent_register_query = Register.query \
        .filter(Register.user_id == current_user.id) \
        .filter(Register.date_time >= start_day_utc) \
        .filter(Register.date_time <= end_day_utc) \
        .order_by(Register.date_time.desc())
    
    pagination = recent_register_query.paginate(page=page, per_page=10)
    recent_registers_medications = pagination.items

    # convertendo data/hora de UTC para Brasilia somente para fim de exibição
    for reg in recent_registers_medications:
        reg.local_time = convert_utc_to_fuso_brasilia(reg.date_time)

    return render_template(
        'medications/recent_registers.html',
        recent_registers=recent_registers_medications,
        pagination=pagination,
        date_chosen=now_timezone_brasilia.date()
    )

@medication_bp.route('/registers/<int:reg_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_register(reg_id):
    # buscando registro
    register = Register.query.get_or_404(reg_id)

    # confirmação que o registro pertence ao usuário logado
    if register.user_id != current_user.id:
        abort(403)

    form = EditRegisterForm(obj=register)

    if form.validate_on_submit():
        register.amount_administered = form.amount_administered.data
        register.observation = form.observation.data

        db.session.commit()
        flash('Registro atualizado com sucesso!', 'success')
        return redirect(url_for('medication.view_history'))
    
    return render_template('medications/edit_register.html', form=form, register=register)

@medication_bp.route('/registers/<int:reg_id>/delete', methods=['POST'])
@login_required
def delete_register(reg_id):
    register = Register.query.get_or_404(reg_id)

    if register.user_id != current_user.id:
        abort(403)

    medication = Medication.query.get(register.medication_id)
    if not medication:
        flash('Medicamento não encontrado.', 'danger')
        return redirect(url_for('medication.list_medications'))

    # Ajusta estoque revertendo o uso deletado
    try:
        quantity_used = float(register.amount_administered.replace(',', '.'))
        medication.stock += quantity_used
    except Exception:
        pass  # Se der erro na conversão, ignore e não ajuste estoque

    try:
        db.session.delete(register)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir registro: {str(e)}', 'danger')
        return redirect(url_for('medication.list_medications'))

    flash('Registro excluído com sucesso!', 'info')
    return redirect(url_for('medication.list_medications'))

@medication_bp.route('/reminders', methods=['GET', 'POST'])
@login_required
def reminders():
    now_utc = datetime.now(timezone.utc)
    now_timezone_brasilia = convert_utc_to_fuso_brasilia(now_utc).time()

    # Busca lembretes ativos para o horário atual (exemplo com margem de 5 minutos)
    reminders_now = MedicationReminder.query.filter(
        MedicationReminder.user_id == current_user.id,
        MedicationReminder.active.is_(True),
        MedicationReminder.time.between(
            (datetime.combine(datetime.today(), now_timezone_brasilia) - timedelta(minutes=5)).time(),
            (datetime.combine(datetime.today(), now_timezone_brasilia) + timedelta(minutes=5)).time()
        )
    ).all()

    # Busca todos os lembretes do usuário
    all_reminders = MedicationReminder.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'medications/reminders/reminders.html',
        current_reminders=reminders_now,
        reminders=all_reminders
    )

@medication_bp.route('/reminders/add', methods=['GET', 'POST'])
@login_required
def add_reminder():
    form = ReminderForm()
    form.medication_id.choices = [
        (med.id, med.name) for med in Medication.query.filter_by(user_id=current_user.id).order_by(Medication.name)
    ]

    if form.validate_on_submit():
        reminder = MedicationReminder(
            user_id=current_user.id,
            medication_id=form.medication_id.data,
            time=form.time.data,
            frequency=form.frequency.data,
            active=form.active.data
        )

        db.session.add(reminder)
        db.session.commit()
        flash('Lembrete criado com sucesso!', 'success')
        return redirect(url_for('medication.reminders'))
    
    return render_template(
        'medications/reminders/reminders_add.html',
        form=form,
        actions_url=url_for('medication.add_reminder'),
        button_text='Criar lembrete'
    )

# rota para edição de lembretes
@medication_bp.route('/reminders/<int:reminder_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_reminder(reminder_id):
    reminder = MedicationReminder.query.get_or_404(reminder_id)

    if reminder.user_id != current_user.id:
        abort(403)

    form = ReminderForm(obj=reminder)
    form.medication_id.choices = [
        (med.id, med.name) for med in Medication.query.filter_by(user_id=current_user.id).order_by(Medication.name)
    ]

    if form.validate_on_submit():
        form.populate_obj(reminder)
        db.session.commit()
        flash('Lembrete atualizado com sucesso!', 'success')
        return redirect(url_for('medication.reminders'))
    
    return render_template(
        'medications/reminders/reminders_edit.html',
        form=form,
        actions_url=url_for('medication.edit_reminder', reminder_id=reminder.id),
        button_text='Salvar alterações'
    )

@medication_bp.route('/reminders/<int:reminder_id>/delete', methods=['POST'])
@login_required
def delete_reminder(reminder_id):
    reminder = MedicationReminder.query.get_or_404(reminder_id)

    if reminder.user_id != current_user.id:
        abort(403)

    db.session.delete(reminder)
    db.session.commit()
    flash('Lembrete excluído com sucesso!', 'success')
    return redirect(url_for('medication.reminders'))

@medication_bp.route('/reminders/check', methods=['GET'])
@login_required
def check_reminders_ajax():
    now_utc = datetime.now(timezone.utc)
    now_timezone_brasilia = convert_utc_to_fuso_brasilia(now_utc).time()

    reminders_now = MedicationReminder.query.filter(
        MedicationReminder.user_id == current_user.id,
        MedicationReminder.active.is_(True),
        MedicationReminder.time.between(
            (datetime.combine(datetime.today(), now_timezone_brasilia) - timedelta(minutes=5)).time(),
            (datetime.combine(datetime.today(), now_timezone_brasilia) + timedelta(minutes=5)).time()
        )
    ).all()

    return jsonify([
        {"medication": rem.medication.name, "time": rem.time.strftime("%H:%M")}
        for rem in reminders_now
    ])

# rota para teste.
@medication_bp.route('/recent-mock')
def recent_registers_mock():
    return render_template('medications/recent_registers_mock.html')
