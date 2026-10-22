from app.database.connection import db


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum("paciente", "cuidador", "admin",
        name='rol_usuario_enum'), nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "rol": self.rol
        }
        
    