from datetime import date, time, datetime
from tests.base_test import BaseTestCase
from app.models.usuario import Usuario
from app.models.medicamento import Medicamento
from app.models.tratamiento import Tratamiento
from app.models.registro_toma import RegistroToma
from app.database.connection import db
from app.services.toma_service import marcar_toma

class TestMarcarToma(BaseTestCase):

    def test_transicion_estado_toma_valida(self):
        """
        Prueba Unitaria: Verificar que marcar_toma permita cambiar el estado
        a 'tomada' y registre automáticamente la fecha_hora_toma actual.
        """
        # 1. Arrange: Crear toma en estado pendiente
        paciente = Usuario(nombre="Luis", correo="luis@medicent.com", contrasena_hash="123", rol="paciente")
        med = Medicamento(nombre="Paracetamol", forma_farmaceutica="Tableta")
        db.session.add_all([paciente, med])
        db.session.commit()

        tratamiento = Tratamiento(
            paciente_id=paciente.id,
            medicamento_id=med.id,
            dosis="1 tableta",
            frecuencia_horas=8,
            fecha_inicio=date(2026, 11, 1),
            fecha_fin=date(2026, 11, 2),
            hora_inicial=time(8, 0, 0)
        )
        db.session.add(tratamiento)
        db.session.commit()

        toma = RegistroToma(
            tratamiento_id=tratamiento.id,
            fecha_hora_programada=datetime(2026, 11, 1, 8, 0, 0),
            estado="pendiente"
        )
        db.session.add(toma)
        db.session.commit()

        # 2. Act: Marcar la toma como 'tomada'
        toma_actualizada = marcar_toma(toma_id=toma.id, nuevo_estado="tomada")

        # 3. Assert: Verificar que cambió de estado y tiene fecha_hora_toma
        self.assertEqual(toma_actualizada.estado, "tomada")
        self.assertIsNotNone(toma_actualizada.fecha_hora_toma)

        toma_en_db = db.session.get(RegistroToma, toma.id)
        self.assertEqual(toma_en_db.estado, "tomada")
        self.assertIsNotNone(toma_en_db.fecha_hora_toma)
