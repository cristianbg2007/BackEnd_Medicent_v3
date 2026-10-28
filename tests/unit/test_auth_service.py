
from base_test import BaseTestCase
from app.services.auth_service import registrar_usuario, iniciar_sesion

class TestAuthService(BaseTestCase):
    def test_registro_usuario_exitoso(self):
    #Arrage = preparar los datos o datos de usuario
        nombre = "Esteban"
        correo = "Esteban@gmail.com"
        contrasena = "123456"
        rol = "paciente"
    #Act
        resultado = registrar_usuario(nombre, correo, contrasena, rol)
    #Assert
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, nombre)
        self.assertEqual(resultado.correo, correo)
        self.assertEqual(resultado.rol, rol)


    def test_registro_correo_duplicado(self):
    #Arrage datos de usuario
        nombre= "Juan"
        correo= "juacho@gmail.com"
        contrasena= "juan123456"
        rol= "paciente"

    #Act
        registrio1 = registrar_usuario(nombre,correo, contrasena, rol)
        registrio2 = registrar_usuario(nombre,correo, contrasena ,rol)

    #Assert
        self.assertIsNotNone(registrio1)
        self.assertIsNone(registrio2)

    def test_login_exitoso(self):
    #Arrage datos de usuario 
        nombre="Carlos"
        correo="carlos1@gmail.com"
        contrasena="123456"
        rol="paciente"
    #Act
        registrar_usuario(nombre, correo, contrasena, rol)
        resultado= iniciar_sesion(correo,contrasena)
    #Assert
        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, dict)
        self.assertIn("token", resultado)
        self.assertEqual(resultado.get("nombre"), nombre)
        self.assertEqual(resultado.get("rol"), rol)