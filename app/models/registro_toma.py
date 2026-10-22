from app.database.connection import db

class RegistroToma(db.Model):
    __tablename__ = 'registros_tomas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tratamiento_id = db.Column(db.Integer, db.ForeignKey('tratamientos.id', ondelete='CASCADE'), nullable=False)
    fecha_hora_programada = db.Column(db.DateTime, nullable=False)
    fecha_hora_toma = db.Column(db.DateTime, nullable=True)
    estado = db.Column(
        db.Enum('pendiente', 'tomada', 'omitida', 'retrasada', name='estado_toma_enum'),
        default='pendiente',
        nullable=False
    )

    # Relación con el tratamiento
    tratamiento = db.relationship('Tratamiento', backref=db.backref('tomas', lazy=True, cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'tratamiento_id': self.tratamiento_id,
            'fecha_hora_programada': self.fecha_hora_programada.isoformat() if self.fecha_hora_programada else None,
            'fecha_hora_toma': self.fecha_hora_toma.isoformat() if self.fecha_hora_toma else None,
            'estado': self.estado
        }
