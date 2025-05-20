from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Medication
from app.forms import MedicationForm

medication_bp = Blueprint('medication', __name__)

@medication_bp.route('/medications')
@login_required
def list_medications():
    medications = Medication.query.all()
    return render_template('medications/list.html', medications=medications)

@medication_bp.route('/medications/add', methods=['GET', 'POST'])
@login_required
def add_medication():
    form = MedicationForm()
    if form.validate_on_submit():
        medication = Medication(
            name = form.name.data,
            description = form.description.data,
            dosage = form.dosage.data,
            hour = form.hour.data,
            stock = form.stock.data
        )
        db.session.add(medication)
        db.session.commit()
        flash('Medicamento adicionado com sucesso!', 'success')
        return redirect(url_for('medication.list_medications'))
    return render_template('medications/add.html', form=form, title='Adicionar Medicamento')

@medication_bp.route('/medications/edit/<int:med_id>', methods=['GET', 'POST'])
@login_required
def edit_medication(med_id):
    medication = Medication.query.get_or_404(med_id)
    form = MedicationForm(obj=medication)
    if form.validate_on_submit():
        form.populate_obj(medication)
        db.session.commit()
        flash('Medicamento atualizado com sucesso!', 'success')
        return redirect(url_for('medication.list_medications'))
    return render_template('medications/edit.html', form=form, title='Editar Medicamento', medication=medication)

@medication_bp.route('/medications/delete/<int:med_id>', methods=['POST'])
@login_required
def delete_medication(med_id):
    medication = Medication.query.get_or_404(med_id)
    db.session.delete(medication)
    db.session.commit()
    flash('Medicamento removido com sucesso!', 'info')
    return redirect(url_for('medication.list_medications'))
