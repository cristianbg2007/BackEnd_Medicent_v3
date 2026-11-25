from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def rol_requerido(*roles_permitidos):
    def decorador(acesso):
        @wraps(acesso)
        def envoltura(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            rol = claims.get("rol")
            if rol not in roles_permitidos:
                return jsonify({"error": "no tienes pérmiso para esta acción"}), 403
            return acesso(*args, **kwargs)

        return envoltura

    return decorador
