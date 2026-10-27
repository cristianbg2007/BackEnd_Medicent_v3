from tests.base_test import BaseTestCase
from app.services.medicamento_service import crear_medicamento

class TestMedicamentoRoutes(BaseTestCase):

    def test_crear_medicamento_endpoint_exitoso(self):
        """POST /api/medicamentos debe crear el medicamento y retornar 201."""
        payload = {
            "nombre": "Amoxicilina",
            "descripcion": "Antibiótico de amplio espectro",
            "forma_farmaceutica": "Cápsula 500mg"
        }
        response = self.client.post("/api/medicamentos", json=payload)

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("mensaje", data)
        self.assertEqual(data["medicamento"]["nombre"], "Amoxicilina")
        self.assertIsNotNone(data["medicamento"]["id"])

    def test_crear_medicamento_sin_nombre_retorna_400(self):
        """POST /api/medicamentos sin nombre obligatorio debe retornar 400."""
        payload = {
            "descripcion": "Sin nombre",
            "forma_farmaceutica": "Tableta"
        }
        response = self.client.post("/api/medicamentos", json=payload)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_listar_medicamentos_endpoint(self):
        """GET /api/medicamentos debe retornar 200 y la lista de medicamentos."""
        crear_medicamento(nombre="Paracetamol", forma_farmaceutica="Comprimido")
        crear_medicamento(nombre="Ibuprofeno", forma_farmaceutica="Cápsula")

        response = self.client.get("/api/medicamentos")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        nombres = [m["nombre"] for m in data]
        self.assertIn("Paracetamol", nombres)
        self.assertIn("Ibuprofeno", nombres)
