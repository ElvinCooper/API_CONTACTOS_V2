import os
from dotenv import load_dotenv
from datetime import timedelta



class BaseConfig:
    # Configurar tiempos de expiración para los tokens
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret")
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    API_TITLE = "API REST Contactos"
    API_VERSION = "v2.0.0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


class DockerConfig(BaseConfig):
    
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    # ...