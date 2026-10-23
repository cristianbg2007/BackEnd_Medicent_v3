from flask import Blueprint
from app.controllers.toma_controller import (
    marcar_toma_controller,
    listar_tomas_paciente_controller
)

toma_bp = Blueprint("toma_bp", __name__, url_prefix="/api/tomas")

toma_bp.route("/<int:toma_id>", methods=["PATCH"])(marcar_toma_controller)
toma_bp.route("/paciente/<int:paciente_id>", methods=["GET"])(listar_tomas_paciente_controller)
