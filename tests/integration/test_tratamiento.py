from datetime import date, time
from base_test import BaseTestCase
from app.models.medicamento import Medicamento
from app.models.usuario import Usuario
from app.models.tratamiento import Tratamiento
from app.database.connection import db

class TestModeloTratamiento(BaseTestCase):

    def test_creacion_modelo_tratamiento(self):
        """Prueba que un Tratamiento se asocie a un Usuario y Medicamento correctamente"""
        # 1. Arrange: Crear usuario y medicamento requeridos por clave foránea
        paciente = Usuario(
            nombre="Juan Perez",
            correo="juan@medicent.com",
            contrasena_hash="hash123",
            rol="paciente"
        )
        med = Medicamento(
            nombre="Ibuprofeno",
            descripcion="Antiinflamatorio",
            forma_farmaceutica="Cápsula"
        )
        db.session.add_all([paciente, med])
        db.session.commit()

        # 2. Act: Crear tratamiento
        tratamiento = Tratamiento(
            paciente_id=paciente.id,
            medicamento_id=med.id,
            dosis="1 cápsula",
            frecuencia_horas=8,
            fecha_inicio=date(2026, 11, 1),
            fecha_fin=date(2026, 11, 7),
            hora_inicial=time(8, 0, 0)
        )
        db.session.add(tratamiento)
        db.session.commit()

        # 3. Assert: Verificar persistencia y relación
        guardado = db.session.get(Tratamiento, tratamiento.id)
        self.assertIsNotNone(guardado)
        self.assertEqual(guardado.paciente.nombre, "Juan Perez")
        self.assertEqual(guardado.medicamento.nombre, "Ibuprofeno")
        self.assertEqual(guardado.dosis, "1 cápsula")
