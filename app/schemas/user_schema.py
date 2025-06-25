from marshmallow import fields, validate, Schema, pre_dump, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models.users_model import Usuario
from datetime import datetime


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
                        
    id       = fields.String(dump_only=True)  
    username = auto_field(required=True, validate=validate.Length(min=1, max=60))
    email    = fields.Email(required=True) 
    password = auto_field(required=True, validate=validate.Length(min=8, max=25))
    
    
    
class UserCreateSchema(Schema):

    username = fields.String(required=True, validate=validate.Length(min=1, max=80))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=200), load_only=True)    
    
    
    
class UserResponseSchema(Schema):
    id = fields.String()
    username = fields.String()
    email = fields.Email()    
    
    
# ------------------------  Schema para registrar un usuario ---------------------------------#    
class UserRegisterSchema(Schema):

    username = fields.String(required=True, validate=validate.Length(min=1, max=60))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=25), load_only=True)    
    