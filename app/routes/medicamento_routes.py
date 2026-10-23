from flask import Blueprint
from app.controllers.medicamento_controller import (
    crear_medicamento_controller,
    listar_medicamentos_controller
)

medicamento_bp = Blueprint("medicamento_bp", __name__, url_prefix="/api/medicamentos")

medicamento_bp.route("", methods=["POST"])(crear_medicamento_controller)
medicamento_bp.route("", methods=["GET"])(listar_medicamentos_controller)
