from datetime import date, time

from flask import jsonify, request

from app.services.tratamiento_service import (
    crear_tratamiento,
    eliminar_tratamiento,
    obtener_tratamientos_por_paciente,
)


def crear_tratamiento_controller():
    """Maneja la creación de prescripción médica y autogeneración de tomas."""
    data = request.get_json() or {}

    paciente_id = data.get("paciente_id")
    medicamento_id = data.get("medicamento_id")
    dosis = data.get("dosis")
    frecuencia_horas = data.get("frecuencia_horas")
    fecha_inicio_str = data.get("fecha_inicio")
    fecha_fin_str = data.get("fecha_fin")
    hora_inicial_str = data.get("hora_inicial")

    # Validación de campos obligatorios
    campos_obligatorios = [
        paciente_id,
        medicamento_id,
        dosis,
        frecuencia_horas,
        fecha_inicio_str,
        fecha_fin_str,
        hora_inicial_str,
    ]
    if any(c is None for c in campos_obligatorios):
        return (
            jsonify({"error": "Todos los campos del tratamiento son obligatorios."}),
            400,
        )

    try:
        fecha_inicio = date.fromisoformat(fecha_inicio_str)
        fecha_fin = date.fromisoformat(fecha_fin_str)
        hora_inicial = time.fromisoformat(hora_inicial_str)
        frecuencia_horas = int(frecuencia_horas)

        nuevo_tratamiento = crear_tratamiento(
            paciente_id=paciente_id,
            medicamento_id=medicamento_id,
            dosis=dosis,
            frecuencia_horas=frecuencia_horas,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            hora_inicial=hora_inicial,
        )

        return (
            jsonify(
                {
                    "mensaje": "Tratamiento creado exitosamente con sus tomas programadas.",
                    "tratamiento": nuevo_tratamiento.to_dict(),
                    "total_tomas_generadas": len(nuevo_tratamiento.tomas),
                }
            ),
            201,
        )

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"Error interno al procesar el tratamiento.": str(e)}), 500


def listar_tratamientos_paciente_controller(paciente_id):
    """Retorna los tratamientos asociados a un paciente en formato JSON."""
    tratamientos = obtener_tratamientos_por_paciente(paciente_id)
    return jsonify([t.to_dict() for t in tratamientos]), 200


def eliminar_tratamiento_controller(tratamiento_id):
    """Elimina un tratamiento específico y todas sus tomas vinculadas."""
    try:
        eliminar_tratamiento(tratamiento_id)
        return (
            jsonify(
                {"mensaje": f"Tratamiento #{tratamiento_id} eliminado exitosamente."}
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"Error interno al eliminar el tratamiento.": str(e)}), 500
