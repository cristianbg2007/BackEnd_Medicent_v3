from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

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
