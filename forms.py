from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, FieldList, FormField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar Sesión")

class RegistroUsuarioForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    role = StringField("Rol", default='user', validators=[DataRequired()])
    submit = SubmitField("Registrarse")

# Formulario para agregar un ingrediente manualmente
class IngredienteForm(FlaskForm):
    nombre = StringField("Nombre del ingrediente", validators=[DataRequired()])
    submit = SubmitField("Agregar")

class IngredienteRecetaForm(FlaskForm):
    ingrediente_id = SelectField("Ingrediente", coerce=int, validators=[DataRequired()])
    cantidad = FloatField("Cantidad", validators=[DataRequired()])

class RecetaForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    ingredientes = FieldList(FormField(IngredienteRecetaForm), min_entries=1)
    submit = SubmitField("Crear Receta")
