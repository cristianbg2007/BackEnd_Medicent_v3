from tests.base_test import BaseTestCase
from app.models.medicamento import Medicamento
from app.database.connection import db

class TestModelosClinicos(BaseTestCase):

    def test_creacion_modelo_medicamento(self):
        """Prueba que un Medicamento se cree en BD y devuelva to_dict()"""
        # 1. Preparar (Arrange)
        nuevo_medicamento = Medicamento(
            nombre="Paracetamol",
            descripcion="Analgésico y antipirético",
            forma_farmaceutica="Comprimido 500mg"
        )

        # 2. Actuar (Act)
        db.session.add(nuevo_medicamento)
        db.session.commit()

        # 3. Verificar (Assert)
        medicamento_guardado = Medicamento.query.filter_by(nombre="Paracetamol").first()
        self.assertIsNotNone(medicamento_guardado)
        self.assertEqual(medicamento_guardado.forma_farmaceutica, "Comprimido 500mg")
        
        datos_dict = medicamento_guardado.to_dict()
        self.assertEqual(datos_dict["nombre"], "Paracetamol")
