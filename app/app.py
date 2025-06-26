from flask import Flask
from flask_cors import CORS
#from app.models.users_model import Usuario
#from app.models.contacts_model import Contacto
#from app.routes.contact_rutes import contacto_bp
from app.rutes.user_routes import usuario_bp
from extensions import db, init_extensions, migrate
from flask_migrate import Migrate
from dotenv import load_dotenv
import os



def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    # Carga la configuración adecuada para Docker
    app.config.from_object('config.DockerConfig') # O la que uses para el entorno Docker

    # ... inicializa db con app ...
    db.init_app(app)

    # Blueprints    
    # app.register_blueprint(contacto_bp, url_prefix='/api')
    app.register_blueprint(usuario_bp , url_prefix='/api/v2')
    
    
    return app
app = create_app()



if __name__ == '__main__':
    app.run(debug=True)