from base_test import BaseTestCase
from app.models.medicamento import Medicamento
from app.database.connection import db

class TestModeloMedicamento(BaseTestCase):

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
