from app.models.usuario import Usuario
from app.models.paciente_cuidador import PacienteCuidador
from app.database.connection import db, bcrypt
from flask_jwt_extended import create_access_token

def registrar_usuario(nombre, correo, contrasena, rol):
    usuario_existe = (Usuario.query.filter_by(correo=correo).first())
    if usuario_existe:
        return None

    contrasena_hash = bcrypt.generate_password_hash(contrasena)

    nuevo_usuario = Usuario(
        nombre= nombre,
        correo = correo,
        contrasena_hash = contrasena_hash,
        rol = rol
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario

def iniciar_sesion(correo,contrasena):
    usuario_existe=(Usuario.query.filter_by(correo=correo).first())
    if not usuario_existe:
        return None
    
    verificar_contrasena = bcrypt.check_password_hash(
        usuario_existe.contrasena_hash,contrasena)
    if verificar_contrasena is False:
        return None

    token = create_access_token(identity=usuario_existe.id, additional_claims={"rol":usuario_existe.rol})
    return {
        "token":token, 
        "id":usuario_existe.id,
        "nombre":usuario_existe.nombre, 
        "rol":usuario_existe.rol
    }

def asignar_paciente(cuidador_id, paciente_id):
    paciente_cuidador_existe = (PacienteCuidador.query.filter_by(cuidador_id=cuidador_id, paciente_id=paciente_id).first())
    if paciente_cuidador_existe:
        return None

    nuevo_paciente_cuidador = PacienteCuidador(
        cuidador_id = cuidador_id,
        paciente_id = paciente_id
    )

    db.session.add(nuevo_paciente_cuidador)
    db.session.commit()
    return nuevo_paciente_cuidador
