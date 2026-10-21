from flask import Flask
from app.config.settings import Config
from app.database.connection import db, bycrypt, jwt
from sqlalchemy import text

def create_app():
    app = Flask(__name__)
    @app.route("/api/estado-db", methods=['GET'])
    def revisar_db():
        db.session.execute(text("select 1"))
        return {"base_de_datos": "conectada"}
    
    #copia los ajustes guardados en la caja de Config
    app.config.from_object(Config)
    #puente de la base de datos 
    db.init_app(app)
    bycrypt.init_app(app)
    jwt.init_app(app)
    
    @app.route("/api/estado", methods=['GET'])
    def revisa_estado():
        return{"estado":"activo"}
        
    return app