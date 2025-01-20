import os
import jwt
import hashlib
from datetime import datetime, timedelta
from psycopg2 import sql

from fastapi import APIRouter, Depends

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.dtos.auth_dto import *
from app.db import get_db


router = APIRouter()

JWT_SECRET = os.environ.get("JWT_SECRET")
ORG_NAME = os.environ.get("ORG_NAME")
print("Vai 12",JWT_SECRET)
# from .authGet import verify_token, verify_user
from .authPost import signup_user, login_user
from .authPatch import update_password
