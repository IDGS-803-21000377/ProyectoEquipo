import os 
from flask_login import config
from sqlalchemy import create_engine 
import urllib
class Config:
    SECRET_KEY = 'clave_nuesa'  
    SECTION_COOKIE_SECURE = False
    UPLOAD_FOLDER = "static/uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1/galletasdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

