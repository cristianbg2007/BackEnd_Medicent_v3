from datetime import date, time, datetime
from base_test import BaseTestCase
from app.models.medicamento import Medicamento
from app.models.usuario import Usuario
from app.models.tratamiento import Tratamiento
from app.models.registro_toma import RegistroToma
from app.database.connection import db

class TestModeloRegistroToma(BaseTestCase):

    def test_creacion_modelo_registro_toma(self):
        """Prueba que un RegistroToma se cree asociado a un Tratamiento con estado pendiente"""
        # 1. Arrange
        paciente = Usuario(
            nombre="Ana Gomez",
            correo="ana@medicent.com",
            contrasena_hash="hash456",
            rol="paciente"
        )
        med = Medicamento(
            nombre="Amoxicilina",
            descripcion="Antibiótico",
            forma_farmaceutica="Suspensión"
        )
        db.session.add_all([paciente, med])
        db.session.commit()

        tratamiento = Tratamiento(
            paciente_id=paciente.id,
            medicamento_id=med.id,
            dosis="5ml",
            frecuencia_horas=12,
            fecha_inicio=date(2026, 11, 1),
            fecha_fin=date(2026, 11, 5),
            hora_inicial=time(9, 0, 0)
        )
        db.session.add(tratamiento)
        db.session.commit()

        # 2. Act: Crear registro de toma
        toma = RegistroToma(
            tratamiento_id=tratamiento.id,
            fecha_hora_programada=datetime(2026, 11, 1, 9, 0, 0),
            estado="pendiente"
        )
        db.session.add(toma)
        db.session.commit()

        # 3. Assert
        toma_guardada = db.session.get(RegistroToma, toma.id)
        self.assertIsNotNone(toma_guardada)
        self.assertEqual(toma_guardada.estado, "pendiente")
        self.assertIsNone(toma_guardada.fecha_hora_toma)
        self.assertEqual(toma_guardada.tratamiento.dosis, "5ml")
