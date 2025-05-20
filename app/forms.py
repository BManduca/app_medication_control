from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class MedicationForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField('Descrição')
    dosage = StringField('Dosagem')
    hour = StringField('Horário')
    stock = IntegerField('Estoque')
    submit = SubmitField('Salvar')
