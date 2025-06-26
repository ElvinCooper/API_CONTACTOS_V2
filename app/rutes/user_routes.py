from flask_smorest import Blueprint, abort
from app.models.users_model import Usuario
from app.schemas.user_schema import UserSchema, UserResponseSchema, UserRegisterSchema, UserCreateSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import HTTPException
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
#from modelos.TokenBlocklist_model import TokenBlocklist
from flask.views import MethodView
from flask import current_app
import traceback
import uuid
from datetime import datetime, timezone
from app.schemas.error_schema import ErrorSchema
from sqlalchemy.exc import IntegrityError


usuario_bp = Blueprint('usuarios', __name__, description="Operaciones con Usuarios")  

@usuario_bp.route('/usuarios')
class UsuarioResource(MethodView):
    #@jwt_required()
    @usuario_bp.response(HTTPStatus.OK, UserResponseSchema(many=True))
    @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
    @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
    
    def get(self):
        """ Consultar todos los usuarios"""
        usuarios = Usuario.query.all()
    
        return usuarios
    
    
# --------------------------------- Consultar un usuario por su id ---------------------------------#   
@usuario_bp.route('/usuarios/<string:id_usuario>')
class UserRegister(MethodView):
    #@jwt_required()    
    @usuario_bp.response(HTTPStatus.OK, UserResponseSchema)
    @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
    @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})    
    def get(self, id_usuario):
        """ Consultar un usuarios por su ID """
        
        try:
            usuario = Usuario.query.filter_by(id=id_usuario).first()
            if not usuario:
                abort(HTTPStatus.NOT_FOUND, message="No existe un usuario con ese id")         
                       
                
            return usuario 
        
        except HTTPException as http_exc:
            raise http_exc  
        except ValueError as e:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Error de valor: {str(e)}")
        except Exception as err:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Error interno del servidor: {str(err)}")  
            
            
            
    
# --------------------------------- Registrar un usuario ---------------------------------#      
@usuario_bp.route('/usuarios')
class UserRegister(MethodView):
    #@jwt_required()
    @usuario_bp.arguments(UserCreateSchema)
    @usuario_bp.response(HTTPStatus.CREATED, UserCreateSchema)
    @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
    @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})    
    def post(self, json_data):
        """ Registrar un nuevo usuario """
        
        try:
            current_app.logger.exception("Error: email duplicado al intentar registrar usuario")
            if Usuario.query.filter_by(email=json_data['email']).first():
               abort(HTTPStatus.BAD_REQUEST, message="Ya existe un usuario con ese email.")
            
            current_app.logger.exception("Error: username duplicado al intentar registrar usuario")
            if Usuario.query.filter_by(username=json_data['username']).first():
                abort(HTTPStatus.BAD_REQUEST, message="Ya existe un usuario con ese nombre.")
   
            
            
           
            nuevo_usuario = Usuario(id = str(uuid.uuid4()),
                                    username= json_data['username'],
                                    email=json_data['email'],
                                    password=generate_password_hash(json_data['password'])
                                    )
            # guardar el nuevo usuario en la base de datos
            db.session.add(nuevo_usuario)
            db.session.commit()          
            
            print("Usuario a serializar:", nuevo_usuario)
            print("Campos:", nuevo_usuario.__dict__)
              
            
            schema = UserResponseSchema()
            return schema.dump(nuevo_usuario), HTTPStatus.CREATED
        
        except IntegrityError as e:
            db.session.rollback()
            if "usuarios_email_key" in str(e.orig):
                abort(HTTPStatus.BAD_REQUEST, message="El email ya está registrado.")
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Violación de integridad en la base de datos.")
            
        except HTTPException as http_exc:
            raise http_exc    
        
        except Exception as err:
            db.session.rollback() # para que se revierta la sesion en caso de algun error.
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Error interno del servidor: {str(err)}")
           
           
    