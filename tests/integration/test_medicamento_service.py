from base_test import BaseTestCase
from app.services.medicamento_service import (
    crear_medicamento,
    obtener_medicamentos,
    obtener_medicamento_por_id
)

class TestMedicamentoService(BaseTestCase):

    def test_crear_medicamento_exitoso(self):
        """Debe crear y persistir un medicamento con datos válidos."""
        med = crear_medicamento(
            nombre="Ibuprofeno",
            descripcion="Antiinflamatorio no esteroideo",
            forma_farmaceutica="Cápsula 400mg"
        )
        self.assertIsNotNone(med.id)
        self.assertEqual(med.nombre, "Ibuprofeno")
        self.assertEqual(med.forma_farmaceutica, "Cápsula 400mg")

    def test_crear_medicamento_sin_nombre_lanza_error(self):
        """Debe rechazar la creación si el nombre está vacío o no se proporciona."""
        with self.assertRaises(ValueError) as context:
            crear_medicamento(
                nombre="",
                descripcion="Sin nombre",
                forma_farmaceutica="Tableta"
            )
        self.assertIn("nombre", str(context.exception).lower())

    def test_obtener_medicamentos_retorna_lista(self):
        """Debe retornar el listado completo de medicamentos registrados."""
        crear_medicamento(nombre="Amoxicilina", forma_farmaceutica="Jarabe")
        crear_medicamento(nombre="Omeprazol", forma_farmaceutica="Cápsula")

        medicamentos = obtener_medicamentos()
        self.assertEqual(len(medicamentos), 2)
        nombres = [m.nombre for m in medicamentos]
        self.assertIn("Amoxicilina", nombres)
        self.assertIn("Omeprazol", nombres)

    def test_obtener_medicamento_por_id_existente_e_inexistente(self):
        """Debe retornar el medicamento si existe, o None si no existe."""
        med_creado = crear_medicamento(nombre="Loratadina", forma_farmaceutica="Comprimido")

        med_encontrado = obtener_medicamento_por_id(med_creado.id)
        self.assertIsNotNone(med_encontrado)
        self.assertEqual(med_encontrado.nombre, "Loratadina")

        med_inexistente = obtener_medicamento_por_id(9999)
        self.assertIsNone(med_inexistente)
