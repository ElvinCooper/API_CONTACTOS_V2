from flask import Flask
from flask_cors import CORS
from models.users_model import Usuario
from models.contacts_model import Contacto
#from routes.contact_rutes import contacto_bp
#from routes.user_rutes import usuario_bp
from extensions import db, init_extensions, migrate
from flask_migrate import Migrate
from dotenv import load_dotenv
import os





# app.py
def create_app():
    app = Flask(__name__)
    # Carga la configuración adecuada para Docker
    app.config.from_object('config.DockerConfig') # O la que uses para el entorno Docker

    # ... inicializa db con app ...
    # db.init_app(app)


    # Blueprints    
    # app.register_blueprint(contacto_bp, url_prefix='/api')
    # app.register_blueprint(usuario_bp , url_prefix='/api')
    
    
    return app











if __name__ == '__main__':
    app.run(debug=True)