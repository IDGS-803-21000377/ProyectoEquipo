from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    FloatField,
    SubmitField,
    FieldList,
    FormField
)

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    password = PasswordField("Contraseña", validators=[validators.DataRequired()])
    submit = SubmitField("Iniciar Sesión")

class RegistroUsuarioForm(FlaskForm):
    username = StringField("Usuario", validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    password = PasswordField("Contraseña", validators=[validators.DataRequired()])
    role = StringField("Rol", default='user', validators=[validators.DataRequired()])
    submit = SubmitField("Registrarse")

class IngredienteForm(FlaskForm):
    ingrediente_id = SelectField('Ingrediente', coerce=int, validators=[DataRequired()])
    cantidad = FloatField('Cantidad', validators=[DataRequired()])


class RecetaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    ingredientes = FieldList(FormField(IngredienteForm), min_entries=1)
    submit = SubmitField('Crear Receta')
