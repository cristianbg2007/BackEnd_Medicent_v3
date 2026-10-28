from datetime import date, time, datetime
from base_test import BaseTestCase
from app.services.toma_service import calcular_horarios_tomas

class TestCalculoTomas(BaseTestCase):

    def test_algoritmo_calculo_tomas_intervalo_regular(self):
        """
        Prueba Unitaria: Comprobar la matemática del motor de tomas:
        Para un tratamiento de 2 días cada 8 horas, debe generar exactamente 6 tomas.
        """
        # 1. Preparar (Arrange)
        fecha_inicio = date(2026, 11, 1)
        fecha_fin = date(2026, 11, 2)
        hora_inicial = time(8, 0, 0)
        frecuencia_horas = 8

        # 2. Actuar (Act)
        horarios = calcular_horarios_tomas(fecha_inicio, fecha_fin, hora_inicial, frecuencia_horas)

        # 3. Verificar (Assert)
        # 2 días (48 horas) / 8 horas = exactamente 6 tomas
        self.assertEqual(len(horarios), 6)

        # Validamos que el primer horario sea exactamente el de inicio
        self.assertEqual(horarios[0], datetime(2026, 11, 1, 8, 0, 0))
        # Validamos que el intervalo entre cada toma sea exactamente de 8 horas
        for i in range(1, len(horarios)):
            diferencia_horas = (horarios[i] - horarios[i-1]).total_seconds() / 3600
            self.assertEqual(diferencia_horas, 8)
