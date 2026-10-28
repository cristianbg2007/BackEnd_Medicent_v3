from datetime import date, time
from base_test import BaseTestCase
from app.models.usuario import Usuario
from app.models.medicamento import Medicamento
from app.services.tratamiento_service import crear_tratamiento
from app.database.connection import db

class TestTomaRoutes(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.paciente = Usuario(nombre="Mario", correo="mario@medicent.com", contrasena_hash="123", rol="paciente")
        self.med = Medicamento(nombre="Ibuprofeno", forma_farmaceutica="Tableta")
        db.session.add_all([self.paciente, self.med])
        db.session.commit()

        # Creamos tratamiento que autogenera 6 tomas
        self.tratamiento = crear_tratamiento(
            paciente_id=self.paciente.id,
            medicamento_id=self.med.id,
            dosis="1 tableta",
            frecuencia_horas=8,
            fecha_inicio=date(2026, 11, 1),
            fecha_fin=date(2026, 11, 2),
            hora_inicial=time(8, 0, 0)
        )
        self.primera_toma = self.tratamiento.tomas[0]

    def test_marcar_toma_endpoint_exitoso(self):
        """PATCH /api/tomas/<id> con nuevo_estado='tomada' retorna 200 y actualiza la toma."""
        payload = {"nuevo_estado": "tomada"}
        response = self.client.patch(f"/api/tomas/{self.primera_toma.id}", json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("toma", data)
        self.assertEqual(data["toma"]["estado"], "tomada")
        self.assertIsNotNone(data["toma"]["fecha_hora_toma"])

    def test_marcar_toma_estado_invalido_retorna_400(self):
        """PATCH /api/tomas/<id> con estado desconocido debe retornar 400."""
        payload = {"nuevo_estado": "inventado"}
        response = self.client.patch(f"/api/tomas/{self.primera_toma.id}", json=payload)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_marcar_toma_inexistente_retorna_404(self):
        """PATCH /api/tomas/99999 debe retornar 404."""
        payload = {"nuevo_estado": "tomada"}
        response = self.client.patch("/api/tomas/99999", json=payload)

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)

    def test_listar_tomas_por_paciente_endpoint(self):
        """GET /api/tomas/paciente/<id> retorna 200 y el listado de tomas del paciente."""
        response = self.client.get(f"/api/tomas/paciente/{self.paciente.id}")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 6)
        self.assertEqual(data[0]["estado"], "pendiente")
