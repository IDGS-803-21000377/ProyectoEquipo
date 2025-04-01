from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, PasswordField, SubmitField
from wtforms import DateField, IntegerField, StringField, PasswordField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired, Optional
from wtforms.validators import DataRequired, Optional
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
    nombre = StringField("Nombre del Ingrediente", validators=[DataRequired()])
    submit = SubmitField("Agregar Ingrediente")

class RecetaForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    ingredientes = FieldList(FormField(IngredienteForm), min_entries=1)
    submit = SubmitField("Crear Receta")



class GalletaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[Optional()])
    existencias = IntegerField('Existencias', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired()])
    gramaje = StringField('Gramaje', validators=[Optional()])
    vidaAnaquel = DateField('Vida Anaquel', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Agregar Galleta')

class GalletaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[Optional()])
    existencias = IntegerField('Existencias', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired()])
    gramaje = FloatField('Gramaje', validators=[Optional()])
    vidaAnaquel = DateField('Vida Anaquel', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Agregar Galleta')


class MaterialForm(FlaskForm):
    nombreProducto = StringField('Nombre del Producto', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    fechaCaducidad = DateField('Fecha de Caducidad', validators=[DataRequired()])
    submit = SubmitField('Guardar')