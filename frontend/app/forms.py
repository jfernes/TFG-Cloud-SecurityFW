from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, FileField)
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class sslaForm(FlaskForm):
    file = FileField('file')
    