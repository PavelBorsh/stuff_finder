from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from models import User


class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()],
                           render_kw={'class': 'input100', 'placeholder': 'Имя пользователя'})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={'class': 'input100', 'placeholder': 'Пароль'})
    remember_me = BooleanField('Запомнить меня', render_kw={'class': 'checkbox mb-1'})
    submit = SubmitField('Войти', render_kw={'class': 'login100-form-btn'})


class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()],
                           render_kw={'class': 'form-control', 'placeholder': 'Имя', 'style': 'border-radius:0%;'})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={'class': 'form-control', 'placeholder': 'Электронный адрес', 'style': 'border-radius:0%;'})
    password = PasswordField(
        'Пароль', validators=[DataRequired()],
        render_kw={'class': 'form-control', 'placeholder': 'Пароль', 'style': 'border-radius:0%;'})
    password2 = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')],
        render_kw={'class': 'form-control', 'placeholder': 'Повторите пароль', 'style': 'border-radius:0%;'})
    submit = SubmitField('Отправить', render_kw={'class': 'login100-form-btn'})

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).count():
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).count():
            raise ValidationError('Пользователь с таким адресом почты уже существует.')
        if email.data == '':
            raise ValidationError('Введите email-адрес')
