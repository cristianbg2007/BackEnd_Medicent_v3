from flask import Blueprint
from app.controllers.tratamiento_controller import (
    crear_tratamiento_controller,
    listar_tratamientos_paciente_controller
)

tratamiento_bp = Blueprint("tratamiento_bp", __name__, url_prefix="/api/tratamientos")

tratamiento_bp.route("", methods=["POST"])(crear_tratamiento_controller)
tratamiento_bp.route("/paciente/<int:paciente_id>", methods=["GET"])(listar_tratamientos_paciente_controller)
