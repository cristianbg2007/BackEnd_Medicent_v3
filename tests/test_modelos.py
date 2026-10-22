from datetime import date, time, datetime
from tests.base_test import BaseTestCase
from app.models.medicamento import Medicamento
from app.models.usuario import Usuario
from app.models.tratamiento import Tratamiento
from app.models.registro_toma import RegistroToma
from app.database.connection import db

class TestModelosClinicos(BaseTestCase):

    def test_creacion_modelo_medicamento(self):
        """Prueba que un Medicamento se cree en BD y devuelva to_dict()"""
        nuevo_medicamento = Medicamento(
            nombre="Paracetamol",
            descripcion="Analgésico y antipirético",
            forma_farmaceutica="Comprimido 500mg"
        )
        db.session.add(nuevo_medicamento)
        db.session.commit()

        medicamento_guardado = Medicamento.query.filter_by(nombre="Paracetamol").first()
        self.assertIsNotNone(medicamento_guardado)
        self.assertEqual(medicamento_guardado.forma_farmaceutica, "Comprimido 500mg")
        self.assertEqual(medicamento_guardado.to_dict()["nombre"], "Paracetamol")

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
