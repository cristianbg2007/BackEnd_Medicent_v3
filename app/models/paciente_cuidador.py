from app.database.connection import db
from datetime import datetime

class PacienteCuidador(db.Model):
    __tablename__ = 'pacientes_cuidadores'

    cuidador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key= True, nullable=False )
    paciente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key= True, nullable=False )
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return{
            "cuidador_id":self.cuidador_id,
            "paciente_id":self.paciente_id,
            "creado_en":self.creado_en,
        }