from app.database.connection import db

class Tratamiento(db.Model):
    __tablename__ = 'tratamientos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamentos.id'), nullable=False)
    dosis = db.Column(db.String(100), nullable=False)
    frecuencia_horas = db.Column(db.Integer, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    hora_inicial = db.Column(db.Time, nullable=False)

    # Relaciones de navegación útiles
    paciente = db.relationship('Usuario', backref=db.backref('tratamientos', lazy=True))
    medicamento = db.relationship('Medicamento', backref=db.backref('tratamientos', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'medicamento_id': self.medicamento_id,
            'dosis': self.dosis,
            'frecuencia_horas': self.frecuencia_horas,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'hora_inicial': self.hora_inicial.isoformat() if self.hora_inicial else None
        }
