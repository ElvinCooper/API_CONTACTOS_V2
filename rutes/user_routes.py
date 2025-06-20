from flask_smorest import Blueprint, abort
from modelos.user_model import Usuario
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import get_jwt
from modelos.TokenBlocklist_model import TokenBlocklist
from flask.views import MethodView
from flask import current_app
import traceback
import uuid
from datetime import datetime, timezone


