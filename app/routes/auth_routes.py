from flask import Blueprint

from app.controllers.auth_controller import (
    asignar_paciente_controller,
    iniciar_sesion_controller,
    registrar_controller,
)

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

auth_bp.route("/registro", methods=["POST"])(registrar_controller)
auth_bp.route("/login", methods=["POST"])(iniciar_sesion_controller)
auth_bp.route("/asignar-paciente", methods=["POST"])(asignar_paciente_controller)
