from datetime import date, time
from base_test import BaseTestCase
from app.models.usuario import Usuario
from app.models.medicamento import Medicamento
from app.database.connection import db

class TestTratamientoRoutes(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.paciente = Usuario(
            nombre="Laura Lopez",
            correo="laura@medicent.com",
            contrasena_hash="hash123",
            rol="paciente"
        )
        self.medicamento = Medicamento(
            nombre="Amoxicilina",
            forma_farmaceutica="Cápsula 500mg"
        )
        db.session.add_all([self.paciente, self.medicamento])
        db.session.commit()

    def test_crear_tratamiento_endpoint_exitoso(self):
        """POST /api/tratamientos debe retornar 201, tratamiento y tomas creadas."""
        payload = {
            "paciente_id": self.paciente.id,
            "medicamento_id": self.medicamento.id,
            "dosis": "500mg",
            "frecuencia_horas": 8,
            "fecha_inicio": "2026-11-01",
            "fecha_fin": "2026-11-02",
            "hora_inicial": "08:00:00"
        }
        response = self.client.post("/api/tratamientos", json=payload)

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("tratamiento", data)
        self.assertEqual(data["tratamiento"]["dosis"], "500mg")
        # 2 días cada 8h = 6 tomas
        self.assertEqual(data["total_tomas_generadas"], 6)

    def test_crear_tratamiento_datos_faltantes_retorna_400(self):
        """POST /api/tratamientos con campos obligatorios vacíos debe retornar 400."""
        payload = {
            "paciente_id": self.paciente.id
            # Faltan medicamento, dosis, fechas, etc.
        }
        response = self.client.post("/api/tratamientos", json=payload)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_listar_tratamientos_por_paciente_endpoint(self):
        """GET /api/tratamientos/paciente/<id> retorna 200 y la lista de tratamientos."""
        # 1. Crear tratamiento primero por el endpoint
        payload = {
            "paciente_id": self.paciente.id,
            "medicamento_id": self.medicamento.id,
            "dosis": "1 tableta",
            "frecuencia_horas": 12,
            "fecha_inicio": "2026-11-01",
            "fecha_fin": "2026-11-03",
            "hora_inicial": "09:00:00"
        }
        self.client.post("/api/tratamientos", json=payload)

        # 2. Consultar tratamientos de la paciente
        response = self.client.get(f"/api/tratamientos/paciente/{self.paciente.id}")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["dosis"], "1 tableta")
