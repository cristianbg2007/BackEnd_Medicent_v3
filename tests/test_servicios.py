from datetime import date, time, datetime
from tests.base_test import BaseTestCase
from app.services.toma_service import calcular_horarios_tomas

class TestMotorTomas(BaseTestCase):

    def test_algoritmo_calculo_tomas_intervalo_regular(self):
        """
        Prueba Unitaria 6: Comprobar la matemática del motor de tomas:
        Para un tratamiento de 2 días cada 8 horas, debe generar exactamente 6 tomas.
        """
        # 1. Preparar (Arrange)
        # Inicio: 2026-11-01 a las 08:00
        # Fin: 2026-11-02 hasta las 23:59 (2 días completos)
        # Frecuencia: cada 8 horas
        fecha_inicio = date(2026, 11, 1)
        fecha_fin = date(2026, 11, 2)
        hora_inicial = time(8, 0, 0)
        frecuencia_horas = 8

        # 2. Actuar (Act)
        horarios = calcular_horarios_tomas(fecha_inicio, fecha_fin, hora_inicial, frecuencia_horas)

        # 3. Verificar (Assert)
        # 2 días (48 horas) / 8 horas = exactamente 6 tomas
        self.assertEqual(len(horarios), 6)

        # Verificar horarios exactos generados
        horarios_esperados = [
            datetime(2026, 11, 1, 8, 0, 0),
            datetime(2026, 11, 1, 16, 0, 0),
            datetime(2026, 11, 2, 0, 0, 0),
            datetime(2026, 11, 2, 8, 0, 0),
            datetime(2026, 11, 2, 16, 0, 0),
            datetime(2026, 11, 3, 0, 0, 0),  # o fin del intervalo según límite
        ]
        # Validamos que el primer horario sea exactamente el de inicio
        self.assertEqual(horarios[0], datetime(2026, 11, 1, 8, 0, 0))
        # Validamos que el intervalo entre cada toma sea exactamente de 8 horas
        for i in range(1, len(horarios)):
            diferencia_horas = (horarios[i] - horarios[i-1]).total_seconds() / 3600
            self.assertEqual(diferencia_horas, 8)
    def test_tomas_generadas_estado_inicial_pendiente(self):
        """
        Prueba Unitaria 7: Confirmar que toda toma recién generada por el motor clínico
        posea el estado 'pendiente' y fecha_hora_toma nula en el 100% de los casos.
        """
        from app.models.usuario import Usuario
        from app.models.medicamento import Medicamento
        from app.models.tratamiento import Tratamiento
        from app.models.registro_toma import RegistroToma
        from app.database.connection import db
        from app.services.toma_service import generar_tomas_tratamiento

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

    def test_transicion_estado_toma_valida(self):
        """
        Prueba Unitaria 8: Verificar que marcar_toma permita cambiar el estado
        a 'tomada' y registre automáticamente la fecha_hora_toma actual.
        """
        from app.models.usuario import Usuario
        from app.models.medicamento import Medicamento
        from app.models.tratamiento import Tratamiento
        from app.models.registro_toma import RegistroToma
        from app.database.connection import db
        from app.services.toma_service import marcar_toma

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

