import os
import jwt
import hashlib
import pandas as pd
from datetime import datetime, timedelta
from psycopg2 import sql

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.dtos.auth_dto import *
from app.db import get_db

# from app.endpoints.user.utils import *


router = APIRouter()

JWT_SECRET = os.environ.get("JWT_SECRET")
print("JWT_SECRET", JWT_SECRET)

from .userGet import get_users
from .userPost import pull_ldap_users
from .userPut import update_bulk_users, update_user
