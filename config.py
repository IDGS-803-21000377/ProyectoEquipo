import os 
from flask_login import config
from sqlalchemy import create_engine 
import urllib
class Config:
    SECRET_KEY = 'clave_nuesa'  
    SECTION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@127.0.0.1/GalletasDB"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

