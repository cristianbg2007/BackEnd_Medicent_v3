from app.database.connection import db
from app.models.usuario import Usuario
from app.models.medicamento import Medicamento
from app.models.tratamiento import Tratamiento
from app.services.toma_service import generar_tomas_tratamiento

def crear_tratamiento(paciente_id, medicamento_id, dosis, frecuencia_horas, fecha_inicio, fecha_fin, hora_inicial):
    """
    Valida y crea un nuevo tratamiento médico.
    Genera automáticamente el calendario de tomas asociado en estado pendiente.
    """
    if not dosis or not dosis.strip():
        raise ValueError("La dosis es obligatoria.")
    if frecuencia_horas <= 0:
        raise ValueError("La frecuencia en horas debe ser mayor a 0.")
    if fecha_fin < fecha_inicio:
        raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio.")

    # Validar existencia de paciente y medicamento
    paciente = db.session.get(Usuario, paciente_id)
    if not paciente:
        raise ValueError(f"No se encontró el paciente con ID {paciente_id}.")

    medicamento = db.session.get(Medicamento, medicamento_id)
    if not medicamento:
        raise ValueError(f"No se encontró el medicamento con ID {medicamento_id}.")

    # Crear el tratamiento
    nuevo_tratamiento = Tratamiento(
        paciente_id=paciente_id,
        medicamento_id=medicamento_id,
        dosis=dosis.strip(),
        frecuencia_horas=frecuencia_horas,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        hora_inicial=hora_inicial
    )

    db.session.add(nuevo_tratamiento)
    db.session.commit()

    # Generar tomas automáticas con el motor clínico
    generar_tomas_tratamiento(nuevo_tratamiento.id)

    return nuevo_tratamiento


def obtener_tratamientos_por_paciente(paciente_id):
    """
    Retorna la lista de tratamientos de un paciente específico.
    """
    return Tratamiento.query.filter_by(paciente_id=paciente_id).all()


def obtener_tratamiento_por_id(tratamiento_id):
    """
    Busca un tratamiento por su ID.
    """
    return db.session.get(Tratamiento, tratamiento_id)
