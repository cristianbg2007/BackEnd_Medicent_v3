from flask import request, jsonify
from app.services.toma_service import (
    marcar_toma,
    obtener_tomas_por_paciente
)

def marcar_toma_controller(toma_id):
    """Maneja la actualización de estado de una toma médica."""
    data = request.get_json() or {}
    nuevo_estado = data.get("nuevo_estado")

    if not nuevo_estado:
        return jsonify({"error": "El campo 'nuevo_estado' es obligatorio."}), 400

    try:
        toma_actualizada = marcar_toma(toma_id=toma_id, nuevo_estado=nuevo_estado)
        return jsonify({
            "mensaje": f"Toma actualizada a '{nuevo_estado}' con éxito.",
            "toma": toma_actualizada.to_dict()
        }), 200
    except ValueError as e:
        mensaje_error = str(e)
        if "No se encontró" in mensaje_error:
            return jsonify({"error": mensaje_error}), 404
        return jsonify({"error": mensaje_error}), 400
    except Exception as e:
        return jsonify({"error": "Error interno al actualizar la toma."}), 500


def listar_tomas_paciente_controller(paciente_id):
    """Retorna la agenda de tomas de un paciente ordenadas cronológicamente."""
    tomas = obtener_tomas_por_paciente(paciente_id)
    return jsonify([t.to_dict() for t in tomas]), 200
