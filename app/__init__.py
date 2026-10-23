from flask import Flask
from app.config.settings import Config
from app.database.connection import db, migrate, bycrypt, jwt
from sqlalchemy import text
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    # 1. Inicializar la base de datos y extensiones
    db.init_app(app)
    #copia los ajustes guardados en la caja de Config
    app.config.from_object(Config)
    migrate.init_app(app, db)
    bycrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)


    # 2. Modelos para Alembic / migrations
    from .models import medicamento
    from .models import usuario
    from .models import tratamiento
    from .models import registro_toma
    from .models import paciente_cuidador

    # 3. Registrar Blueprints
    from app.routes.medicamento_routes import medicamento_bp
    from app.routes.tratamiento_routes import tratamiento_bp
    app.register_blueprint(medicamento_bp)
    app.register_blueprint(tratamiento_bp)

    @app.route("/api/estado-db", methods=['GET'])
    def revisar_db():
        db.session.execute(text("select 1"))
        return {"base_de_datos": "conectada"}

    @app.route("/api/estado", methods=['GET'])
    def revisa_estado():
        return {"estado": "activo"}

    return app
