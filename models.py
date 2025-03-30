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
    

class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Float, nullable=False)  # cantidad disponible en almacén

class Receta(db.Model):
    __tablename__ = 'receta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)

class RecetaIngrediente(db.Model):
    __tablename__ = 'receta_ingrediente'
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'))
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))
    cantidad = db.Column(db.Float, nullable=False)  # cantidad necesaria

    receta = db.relationship("Receta", backref="ingredientes_rel")
    ingrediente = db.relationship("Ingrediente")


class Galleta(db.Model):
    __tablename__ = 'galleta'  
    idGalleta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(45), nullable=False)
    descripcion = db.Column(db.String(150), nullable=True)
    existencias = db.Column(db.Integer, nullable=True)
    precio = db.Column(db.Float, nullable=True)
    gramaje = db.Column(db.Float, nullable=True)
    vidaAnaquel = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Galleta {self.nombre}>"

