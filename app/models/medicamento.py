from app.database.connection import db

class Medicamento(db.Model):
    __tablename__ = 'medicamentos'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nombre=db.Column(db.String(150),nullable=False)
    descripcion=db.Column(db.String(255), nullable=True)
    forma_farmaceutica= db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return{
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'forma_farmaceutica': self.forma_farmaceutica
        }

        