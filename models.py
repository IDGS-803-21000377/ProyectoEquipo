from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), nullable=False, default="user") 

    UPLOAD_FOLDER = "static/uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

    def get_id(self):
        """Devuelve el ID del usuario para Flask-Login"""
        return str(self.id_user)

    def set_password(self, password):
        """Genera un hash para la contraseña y la guarda"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña comparando el hash"""
        return check_password_hash(self.password, password)
