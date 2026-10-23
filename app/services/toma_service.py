from datetime import datetime, timedelta
from app.database.connection import db
from app.models.tratamiento import Tratamiento
from app.models.registro_toma import RegistroToma

def calcular_horarios_tomas(fecha_inicio, fecha_fin, hora_inicial, frecuencia_horas):
    """
    Calcula la lista de fechas y horas exactas para las tomas de un tratamiento.
    
    Para una duración en días (fecha_fin - fecha_inicio + 1 día), calcula el total
    de horas de cobertura y genera las tomas correspondientes con el intervalo regular.
    """
    if frecuencia_horas <= 0:
        raise ValueError("La frecuencia en horas debe ser mayor a 0.")
    if fecha_fin < fecha_inicio:
        raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio.")

    # 1. Cantidad total de días del tratamiento (ej: del 01 al 02 son 2 días)
    total_dias = (fecha_fin - fecha_inicio).days + 1
    total_horas = total_dias * 24

    # 2. Número de tomas esperadas para la duración completa
    total_tomas = total_horas // frecuencia_horas

    # 3. Generar la lista de horarios iniciando desde (fecha_inicio + hora_inicial)
    momento_actual = datetime.combine(fecha_inicio, hora_inicial)
    horarios = []

    for _ in range(total_tomas):
        horarios.append(momento_actual)
        momento_actual += timedelta(hours=frecuencia_horas)

    return horarios


def generar_tomas_tratamiento(tratamiento_id):
    """
    Busca el tratamiento por su ID, calcula sus horarios regulares y
    crea en la base de datos los registros de tomas con estado inicial 'pendiente'.
    """
    tratamiento = db.session.get(Tratamiento, tratamiento_id)
    if not tratamiento:
        raise ValueError(f"No se encontró el tratamiento con ID {tratamiento_id}.")

    # 1. Calcular todos los timestamps con la función matemática
    horarios = calcular_horarios_tomas(
        fecha_inicio=tratamiento.fecha_inicio,
        fecha_fin=tratamiento.fecha_fin,
        hora_inicial=tratamiento.hora_inicial,
        frecuencia_horas=tratamiento.frecuencia_horas
    )

    tomas_creadas = []

    # 2. Instanciar cada registro de toma
    for horario in horarios:
        toma = RegistroToma(
            tratamiento_id=tratamiento.id,
            fecha_hora_programada=horario,
            fecha_hora_toma=None,
            estado='pendiente'
        )
        db.session.add(toma)
        tomas_creadas.append(toma)

    # 3. Guardar en la base de datos
    db.session.commit()

    return tomas_creadas

def marcar_toma(toma_id, nuevo_estado, fecha_toma=None):
    """
    Actualiza el estado de una toma ('tomada', 'omitida', 'retrasada').
    Si no se proporciona fecha_toma, se asigna automáticamente la fecha y hora actual del sistema.
    """
    estados_validos = {'pendiente', 'tomada', 'omitida', 'retrasada'}
    if nuevo_estado not in estados_validos:
        raise ValueError(f"Estado '{nuevo_estado}' no válido. Opciones: {estados_validos}")

    toma = db.session.get(RegistroToma, toma_id)
    if not toma:
        raise ValueError(f"No se encontró el registro de toma con ID {toma_id}.")

    # 1. Asignar el nuevo estado
    toma.estado = nuevo_estado

    # 2. Registrar la fecha y hora de la toma
    if nuevo_estado in ('tomada', 'retrasada'):
        toma.fecha_hora_toma = fecha_toma if fecha_toma else datetime.utcnow()

    # 3. Guardar cambios en la base de datos
    db.session.commit()

    return toma


def obtener_tomas_por_paciente(paciente_id):
    """
    Retorna la lista de todas las tomas de los tratamientos de un paciente,
    ordenadas por fecha y hora programada.
    """
    return (
        RegistroToma.query
        .join(Tratamiento)
        .filter(Tratamiento.paciente_id == paciente_id)
        .order_by(RegistroToma.fecha_hora_programada.asc())
        .all()
    )

