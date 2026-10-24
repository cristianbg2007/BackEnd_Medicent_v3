from app.services.auth_service import registrar_usuario

def registar(nombre, correo, contrasena, rol):
    datos_registar = registrar_usuario(nombre, correo, contrasena, rol)
    correo_existe = (Usuario.correo.query.filter_by(correo=correo).first())
    if correo_existe:
        return (400)
        pass
    