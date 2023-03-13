from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, FileField)
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class SSLAForm(FlaskForm):
    file = FileField('file')
    