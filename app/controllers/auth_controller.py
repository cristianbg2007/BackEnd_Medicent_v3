from app.services.auth_service import registrar_usuario, iniciar_sesion, asignar_paciente
from flask import request, jsonify
from app.middlewares.auth_middleware import rol_requerido

def registrar_controller():
    data = request.get_json() or {}
    nombre = data.get("nombre")
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    rol = data.get("rol")
    if not nombre:
        return jsonify({"error": "El campo nombre es obligatorio"}), 400
    if not correo:
        return jsonify({"error": "El campo correo es obligatorio"}), 400
    if not contrasena:
        return jsonify({"error": "El campo contraseña es obligatorio"}), 400
    if not rol:
        return jsonify({"error": "El campo rol es obligatorio"}), 400

    resultado = registrar_usuario(nombre, correo, contrasena ,rol)
    if resultado is None:
        return jsonify({"error": "Este correo ya esta regstrado intenten con otro"}), 400

    return jsonify({"mensaje": "Usuario registrado exitosamente",
                "usuario": resultado.to_dict()}), 201

def iniciar_sesion_controller():
    data = request.get_json() or {}
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    if not correo:
        return jsonify({"error": "El campo correo es obligatorio"}), 400
    if not contrasena:
         return jsonify({"error": "El campo contraseña es obligatorio"}), 400
    resultado = iniciar_sesion(correo,contrasena)
    if resultado is None:
        return jsonify({"error": "credenciales incorrectas ingrese bien sus datos"}),401
    return jsonify(resultado),200

@rol_requerido("cuidador", "admin")
def asignar_paciente_controller():
    data = request.get_json() or {}
    cuidador_id = data.get("cuidador_id")
    paciente_id = data.get("paciente_id")

    if cuidador_id is None:
        return jsonify({"error": "El campo cuidador_id es obligatorio"}), 400
    if paciente_id is None:
        return jsonify({"error": "El campo paciente_id es obligatorio"}), 400

    resultado = asignar_paciente(cuidador_id, paciente_id)

    if resultado is None:
        return jsonify({"error": "Esta asignación ya existe"}), 400

    return jsonify({
        "mensaje": "Paciente asignado al cuidador exitosamente",
        "asignacion": resultado.to_dict()
    }), 201