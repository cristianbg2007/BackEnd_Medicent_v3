from app.database.connection import db
from app.models.medicamento import Medicamento

def crear_medicamento(nombre, descripcion=None,forma_farmaceutica=None):
    """Crea y persiste un medicamento en la base de datos"""
    if not nombre or not nombre.strip():
        raise ValueError("El nombre del medicamento es obligatorio")

    nuevo_medicamento = Medicamento(
        nombre=nombre.strip(),
        descripcion=descripcion.strip() if descripcion else None,
        forma_farmaceutica=forma_farmaceutica.strip() if forma_farmaceutica else None)
     
    db.session.add(nuevo_medicamento)
    db.session.commit()
    return nuevo_medicamento

def obtener_medicamentos():
    """
    Retorna la lista de todos los medicamentos en la base de datos.
    """
    return Medicamento.query.all()
def obtener_medicamento_por_id(medicamento_id):
    """
    Busca un medicamento por su ID primario.
    Retorna la instancia si existe o None si no se encuentra.
    """
    return db.session.get(Medicamento, medicamento_id)
