import os

from flask import Flask
from flask_cors import CORS
from sqlalchemy import text

from app.config.settings import Config
from app.database.connection import bcrypt, db, jwt, migrate
from app.routes.auth_routes import auth_bp


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///local.db"
    )
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    # 1. Inicializar la base de datos y extensiones
    db.init_app(app)
    # copia los ajustes guardados en la caja de Config
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 2. Modelos para Alembic / migrations
    # 3. Registrar Blueprints
    from app.routes.medicamento_routes import medicamento_bp
    from app.routes.toma_routes import toma_bp
    from app.routes.tratamiento_routes import tratamiento_bp

    from .models import (  # noqa: F401
        medicamento,
        paciente_cuidador,
        registro_toma,
        tratamiento,
        usuario,
    )

    app.register_blueprint(medicamento_bp)
    app.register_blueprint(tratamiento_bp)
    app.register_blueprint(toma_bp)
    app.register_blueprint(auth_bp)

    @app.route("/api/estado-db", methods=["GET"])
    def revisar_db():
        db.session.execute(text("select 1"))
        return {"base_de_datos": "conectada"}

    @app.route("/api/estado", methods=["GET"])
    def revisa_estado():
        return {"estado": "activo"}

    @app.get("/health")
    def health():
        db.session.execute(text("SELECT 1"))
        return {"status": "ok"}, 200

    return app
