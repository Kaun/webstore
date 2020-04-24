from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField


class OrderForm(FlaskForm):
    name = StringField('Ваше имя', [InputRequired()])
    address = StringField('Адрес', [InputRequired()])
    # client_email = StringField('Электронная почта', [InputRequired(), Email()])
    email = EmailField("Электронная почта", [InputRequired(), Email()])
    phone = StringField('Ваш телефон', [InputRequired()])
    submit = SubmitField('Оформить заказ')


class LoginForm(FlaskForm):
    email = EmailField("Электронная почта", [InputRequired(), Email()])
    pswd = PasswordField("Пароль", [InputRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField("Электронная почта", [InputRequired(), Email()])
    pswd = PasswordField("Пароль", [InputRequired()])
    submit = SubmitField('Зарегистрироваться')
