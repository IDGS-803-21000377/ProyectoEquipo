from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash
from forms import LoginForm, RegistroUsuarioForm
from models import User, db

auth_bp = Blueprint('auth', __name__, url_prefix='') 

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, inicia sesión para continuar."
login_manager.login_message_category = "warning"

# Página principal/inicio
@auth_bp.route('/inicio')
@login_required
def inicio():
    return render_template("index.html")

@auth_bp.route('/index')
@login_required
def index():
    return render_template("index.html")

# Login
@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            print(f"Usuario encontrado: {user}")
            
            if user and user.check_password(form.password.data):
                print(f"Usuario autenticado: {user.username}")
                login_user(user)
                flash("Inicio de sesión exitoso", "success")
                return redirect(url_for('auth.index'))
            else:
                flash("Usuario o contraseña incorrectos", "error")

    return render_template("login.html", form=form)



# Logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

# Dashboard
@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")

# Registro
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroUsuarioForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(form.password.data, method='scrypt')
        
        nuevo_usuario = User(
            username=form.username.data,
            password=hashed_password,
            role=form.role.data 
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Usuario registrado correctamente", "success")
        return redirect(url_for('auth.login'))
    
    return render_template('registro.html', form=form)
