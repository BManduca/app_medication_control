from datetime import date
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, FloatField, SelectField, StringField, IntegerField, TextAreaField, SubmitField, PasswordField, TimeField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Email, EqualTo, ValidationError

class MedicationForm(FlaskForm):
    name = StringField('Nome', validators=[
        DataRequired(message='O nome é obrigatório.'),
        Length(min=2, max=120, message='O nome deve ter no máximo 120 caracteres.')
    ])
    description = TextAreaField('Descrição', validators=[
        Length(max=255, message='A descrição deve ter no máximo 255 caracteres.')
    ])
    dosage = StringField('Dosagem', validators=[
        DataRequired(message='A dosagem é obrigatória.'),
        Length(max=100, message='A dosagem deve ter no máximo 100 caracteres.')
    ])
    expiration_date = DateField('Data de validade',  format='%d/%m/%Y', validators=[
        DataRequired(message='A data de validade é obrigatória.')
    ])

    def validate_expiration_date(self, field: DateField) -> None:
        if field.data and field.data < date.today():
            raise ValidationError('A data de validade não pode ser anterior a data atual. Verifique se o medicamento não está vencido.')

    frequency = StringField('Frequência', validators=[
        Length(max=100, message='A frequência deve ter no máximo 100 caracteres.')
    ])
    hour = TimeField('Horário (opcional)')
    stock = FloatField('Estoque', validators=[
        DataRequired(message='O estoque é obrigatório.'),
        NumberRange(min=0, message='O estoque não pode ser negativo.')
    ])
    instructions = TextAreaField('Instruções de uso', validators=[
        Length(max=255, message='As instruções devem ter no máximo 255 caracteres.')
    ])
    submit = SubmitField('Salvar')

class RegisterUseMedicationForm(FlaskForm):
    quantity = StringField(
        'Quantidade administrada',
        validators=[
            DataRequired(message='Por favor, informe a quantidade administrada.')
        ]
    )
    observation = TextAreaField(
        'Observações',
        validators=[
            Optional(),
            Length(max=255, message='A observação pode ter no máximo 255 caracteres.')
        ]
    )

    submit = SubmitField('Registrar uso')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="O campo e-mail é obrigatório"), 
        Email(message="Digite um e-mail válido.")
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message="O campo senha é obrigatório.")
    ])
    submit = SubmitField('Acessar')

class RegisterForm(FlaskForm):
    username = StringField("Nome de usuário", validators=[
        DataRequired(message="O nome de usuário é obrigatório."),
        Length(max=100, message='O nome de usuário deve ter no máximo 100 caracteres.')
    ])
    email = StringField("Email", validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="Digite um e-mail válido.")
    ])
    password = PasswordField("Senha", validators=[
        DataRequired(message="A senha é obrigatória."),
        Length(min=6, message="A senha deve ter pelo menos 6 caracteres.")
    ])
    confirm_password = PasswordField("Confirme a senha", validators=[
        DataRequired(message="A confirmação da senha é obrigatória."),
        EqualTo('password', message="As senhas devem ser iguais")
    ])
    submit = SubmitField("Cadastrar")

class FilterDateForm(FlaskForm):
    start_date = DateField('Data inicial', format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField('Data final', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Filtrar')

class NameFilterForm(FlaskForm):
    name = StringField('Nome', validators=[Optional()])

class EditRegisterForm(FlaskForm):
    amount_administered = StringField('Quantidade administrada', validators=[Optional()])
    observation = TextAreaField('Observação', validators=[Optional()])
    submit = SubmitField('Salvar')

class ReminderForm(FlaskForm):
    medication_id = SelectField(
        'Medicamento',
        coerce=int,
        validators=[DataRequired(message='Selecione um medicamento.')]
    )
    time = TimeField('Horário', validators=[DataRequired(message='Informe um horário válido para o lembrete.')])
    frequency = SelectField(
        'Frequência',
        choices=[
            ('once', 'Apenas uma vez'),
            ('daily', 'Diariamente'),
            ('weekly', 'Semanalmente')
        ],
        default='once',
        validators=[DataRequired(message='Por favor, selecione a frequência do lembrete.')]
    )
    active = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
