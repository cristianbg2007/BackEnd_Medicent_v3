from datetime import date, time
from tests.base_test import BaseTestCase
from app.models.usuario import Usuario
from app.models.medicamento import Medicamento
from app.database.connection import db
from app.services.tratamiento_service import (
    crear_tratamiento,
    obtener_tratamientos_por_paciente,
    obtener_tratamiento_por_id
)

class TestTratamientoService(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Creamos paciente y medicamento base para las pruebas
        self.paciente = Usuario(
            nombre="Carlos Perez",
            correo="carlos@medicent.com",
            contrasena_hash="hash123",
            rol="paciente"
        )
        self.medicamento = Medicamento(
            nombre="Ibuprofeno",
            descripcion="Antiinflamatorio",
            forma_farmaceutica="Cápsula 400mg"
        )
        db.session.add_all([self.paciente, self.medicamento])
        db.session.commit()

    def test_crear_tratamiento_exitoso_genera_tomas(self):
        """Debe persistir el tratamiento y generar automáticamente sus tomas pendientes."""
        tratamiento = crear_tratamiento(
            paciente_id=self.paciente.id,
            medicamento_id=self.medicamento.id,
            dosis="1 cápsula",
            frecuencia_horas=8,
            fecha_inicio=date(2026, 11, 1),
            fecha_fin=date(2026, 11, 2),
            hora_inicial=time(8, 0, 0)
        )

        self.assertIsNotNone(tratamiento.id)
        self.assertEqual(tratamiento.paciente_id, self.paciente.id)
        self.assertEqual(tratamiento.medicamento_id, self.medicamento.id)
        # 2 días (48h) cada 8h = 6 tomas generadas automáticamente
        self.assertEqual(len(tratamiento.tomas), 6)
        self.assertEqual(tratamiento.tomas[0].estado, "pendiente")

    def test_crear_tratamiento_paciente_inexistente_lanza_error(self):
        """Debe lanzar error si el paciente no existe."""
        with self.assertRaises(ValueError) as ctx:
            crear_tratamiento(
                paciente_id=9999,
                medicamento_id=self.medicamento.id,
                dosis="1 cápsula",
                frecuencia_horas=8,
                fecha_inicio=date(2026, 11, 1),
                fecha_fin=date(2026, 11, 2),
                hora_inicial=time(8, 0, 0)
            )
        self.assertIn("paciente", str(ctx.exception).lower())

    def test_crear_tratamiento_medicamento_inexistente_lanza_error(self):
        """Debe lanzar error si el medicamento no existe."""
        with self.assertRaises(ValueError) as ctx:
            crear_tratamiento(
                paciente_id=self.paciente.id,
                medicamento_id=9999,
                dosis="1 cápsula",
                frecuencia_horas=8,
                fecha_inicio=date(2026, 11, 1),
                fecha_fin=date(2026, 11, 2),
                hora_inicial=time(8, 0, 0)
            )
        self.assertIn("medicamento", str(ctx.exception).lower())

    def test_crear_tratamiento_fechas_o_frecuencia_invalidas(self):
        """Debe validar que fecha_fin no sea anterior a fecha_inicio y frecuencia > 0."""
        # Fechas invertidas
        with self.assertRaises(ValueError):
            crear_tratamiento(
                paciente_id=self.paciente.id,
                medicamento_id=self.medicamento.id,
                dosis="1 cápsula",
                frecuencia_horas=8,
                fecha_inicio=date(2026, 11, 5),
                fecha_fin=date(2026, 11, 1),
                hora_inicial=time(8, 0, 0)
            )

        # Frecuencia en horas inválida (cero o negativa)
        with self.assertRaises(ValueError):
            crear_tratamiento(
                paciente_id=self.paciente.id,
                medicamento_id=self.medicamento.id,
                dosis="1 cápsula",
                frecuencia_horas=0,
                fecha_inicio=date(2026, 11, 1),
                fecha_fin=date(2026, 11, 2),
                hora_inicial=time(8, 0, 0)
            )

    def test_obtener_tratamientos_por_paciente(self):
        """Debe listar todos los tratamientos de un paciente dado."""
        crear_tratamiento(
            paciente_id=self.paciente.id,
            medicamento_id=self.medicamento.id,
            dosis="1 cápsula",
            frecuencia_horas=12,
            fecha_inicio=date(2026, 11, 1),
            fecha_fin=date(2026, 11, 2),
            hora_inicial=time(8, 0, 0)
        )

        tratamientos = obtener_tratamientos_por_paciente(self.paciente.id)
        self.assertEqual(len(tratamientos), 1)
        self.assertEqual(tratamientos[0].dosis, "1 cápsula")

        # Paciente sin tratamientos
        sin_tratamientos = obtener_tratamientos_por_paciente(8888)
        self.assertEqual(len(sin_tratamientos), 0)
