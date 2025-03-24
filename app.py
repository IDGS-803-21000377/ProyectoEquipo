from hashlib import scrypt
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields import PasswordField
from wtforms.validators import InputRequired, Length

from forms import LoginForm
from models import User
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app = Flask(__name__)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/index")
@login_required
def index():
    return f"Bienvenido {current_user.username}! <a href='/logout'>Cerrar sesión</a>"

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and scrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Credenciales incorrectas", "danger")

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))



if __name__ == '__main__':
    app.run(debug=True)