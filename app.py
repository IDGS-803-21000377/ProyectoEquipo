from flask import Flask, flash, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from forms import LoginForm
from models import User, db  

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)  

csrf = CSRFProtect(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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
        if user and user.check_password(form.password.data):
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
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
