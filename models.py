from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        """Método para establecer la contraseña"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Método para verificar la contraseña"""
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return str(self.id_user)
    
    def has_role(self, role):
        """Método para verificar los permisos del usuario"""
        return self.role == role