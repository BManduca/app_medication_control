from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired, Length

class MedicationForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField('Descrição', validators=[Length(max=255)])
    dosage = StringField('Dosagem', validators=[DataRequired()])
    hour = StringField('Horário', validators=[DataRequired()])
    stock = IntegerField('Estoque', validators=[DataRequired()])
    submit = SubmitField('Salvar')
