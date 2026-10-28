import unittest 
from app import create_app
from app.config.settings import TestConfig
from app.database.connection import db 


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # 1. Crea la app en modo de pruebas con SQLite en memoria
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        # 2. Crea las tablas en memoria
        db.create_all()
    def tearDown(self):
        # 3. Limpia la base de datos después de cada prueba
        db.session.remove()
        db.drop_all()
        self.ctx.pop()