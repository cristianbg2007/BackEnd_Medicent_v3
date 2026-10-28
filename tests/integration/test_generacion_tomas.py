from datetime import date, time
from base_test import BaseTestCase
from app.models.usuario import Usuario
from app.models.medicamento import Medicamento
from app.models.tratamiento import Tratamiento
from app.database.connection import db
from app.services.toma_service import generar_tomas_tratamiento

class TestGeneracionTomas(BaseTestCase):

    def test_tomas_generadas_estado_inicial_pendiente(self):
        """
        Prueba Unitaria: Confirmar que toda toma recién generada por el motor clínico
        posea el estado 'pendiente' y fecha_hora_toma nula en el 100% de los casos.
        """
        # 1. Preparar (Arrange): Crear paciente, medicamento y tratamiento
        paciente = Usuario(
            nombre="Carlos Ruiz",
            correo="carlos@medicent.com",
            contrasena_hash="hash123",
            rol="paciente"
        )
        med = Medicamento(
            nombre="Amoxicilina",
            descripcion="Antibiótico",
            forma_farmaceutica="Cápsula 500mg"
        )
        db.session.add_all([paciente, med])
        db.session.commit()

        tratamiento = Tratamiento(
            paciente_id=paciente.id,
            medicamento_id=med.id,
            dosis="500mg",
            frecuencia_horas=8,
            fecha_inicio=date(2026, 11, 1),
            fecha_fin=date(2026, 11, 2),
            hora_inicial=time(8, 0, 0)
        )
        db.session.add(tratamiento)
        db.session.commit()

        # 2. Actuar (Act): Generar y persistir las tomas del tratamiento
        tomas_creadas = generar_tomas_tratamiento(tratamiento.id)

        # 3. Verificar (Assert)
        self.assertEqual(len(tomas_creadas), 6)
        for toma in tomas_creadas:
            self.assertEqual(toma.estado, "pendiente")
            self.assertIsNone(toma.fecha_hora_toma)
            self.assertEqual(toma.tratamiento_id, tratamiento.id)
            self.assertIsNotNone(toma.id)
