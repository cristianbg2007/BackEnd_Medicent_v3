import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS= False

#para las pruebas en (sqlLite)
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "clave-super-secreta-de-pruebas"
    JWT_SECRET_KEY = "jwt-super-secreto-de-pruebas"
    SQLALCHEMY_TRACK_MODIFICATIONS = False