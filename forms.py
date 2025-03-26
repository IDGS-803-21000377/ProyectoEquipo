from wtforms import FloatField, Form, RadioField, SelectMultipleField, SubmitField
from flask_wtf import FlaskForm
 
from wtforms import StringField,IntegerField
from wtforms import EmailField
from wtforms import validators
from wtforms.fields import PasswordField
 
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[validators.InputRequired(), validators.Length(min=3, max=50)])
    password = PasswordField('Contraseña', validators=[validators.InputRequired()])
    submit = SubmitField('Iniciar Sesión')


class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    password = PasswordField("Contraseña", validators=[validators.DataRequired()])
    submit = SubmitField("Iniciar Sesión")
