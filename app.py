from flask import Flask, flash, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from forms import LoginForm
from models import User, db  
from Blueprints.auth.routes import auth_bp
from Blueprints.recetas.routes import recetas_bp
from Blueprints.Inventario.routes import inventario_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)  

csrf = CSRFProtect(app)

db.init_app(app)

with app.app_context():
    db.create_all()  
    
    user = User.query.filter_by(username="luis").first()
    if not user:
        user = User(username="luis")
        user.set_password("1234")  
        db.session.add(user)
        db.session.commit()

    print("Base de datos y usuario 'luis' creados exitosamente.")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(auth_bp)
app.register_blueprint(recetas_bp)
app.register_blueprint(inventario_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
