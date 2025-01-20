import os
import jwt
import hashlib
from datetime import datetime, timedelta
from psycopg2 import sql

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db

# from app.endpoints.user.utils import *
from app.dtos.project_dto import *

router = APIRouter()

from .projectGet import get_all_project_assignments, get_all_projects, get_project_by_id
from .projectPut import update_project, update_project_assign
from .projectPost import create_project, assign_create
