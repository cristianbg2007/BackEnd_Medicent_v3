from flask import Flask
from app.config.settings import Config
from app.database.connection import db, migrate
from sqlalchemy import text

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Inicializar la base de datos y migraciones
    db.init_app(app)
    migrate.init_app(app, db)

    # 2. Modelos para Alembic / migrations
    from .models import medicamento

    # 3. Rutas básicas
    @app.route("/api/estado-db", methods=['GET'])
    def revisar_db():
        db.session.execute(text("select 1"))
        return {"base_de_datos": "conectada"}

    @app.route("/api/estado", methods=['GET'])
    def revisa_estado():
        return {"estado": "activo"}

    return app
