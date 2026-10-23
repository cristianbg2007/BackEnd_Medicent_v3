from flask import request, jsonify
from app.services.medicamento_service import (
    crear_medicamento,
    obtener_medicamentos
)

def crear_medicamento_controller():
    """Maneja la creación de un nuevo medicamento desde la API."""
    data = request.get_json() or {}
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    forma_farmaceutica = data.get("forma_farmaceutica")

    if not nombre or not nombre.strip():
        return jsonify({"error": "El nombre del medicamento es obligatorio."}), 400

    try:
        nuevo_medicamento = crear_medicamento(
            nombre=nombre,
            descripcion=descripcion,
            forma_farmaceutica=forma_farmaceutica
        )
        return jsonify({
            "mensaje": "Medicamento creado exitosamente.",
            "medicamento": nuevo_medicamento.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno al registrar el medicamento."}), 500


def listar_medicamentos_controller():
    """Retorna la lista de todos los medicamentos en formato JSON."""
    medicamentos = obtener_medicamentos()
    return jsonify([med.to_dict() for med in medicamentos]), 200
