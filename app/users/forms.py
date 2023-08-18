from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField
from wtforms.validators import DataRequired, Email, Length,EqualTo

class SingUpForm(FlaskForm):
    name = StringField('Nombre *', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Primer apellido *', validators=[DataRequired(), Length(max=64)])
    second_last_name = StringField('Segundo apellido', validators=[Length(max=64)])
    email = StringField('Email *', validators=[DataRequired(), Email()])            
    password = PasswordField('Password *', validators=[DataRequired(),Length(min=8,max=16,message="Contraseña debe tener entre 8 y 16 caracteres")])
    password_repeat = PasswordField('Repita Password *', validators=[DataRequired(),EqualTo('password',message='Password deben ser identicas')])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')