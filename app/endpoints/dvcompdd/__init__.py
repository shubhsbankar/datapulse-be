import pandas as pd

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db, get_sqlalchemy_conn
from app.dtos.dvcompdd_dto import DvCompDdDTO

router = APIRouter()

from .dvcompddGet import get_all_dvcompdd
from .dvcompddPost import create_dvcompdd, test_dvcompdd, get_table_columns
from .dvcompddPut import update_dvcompdd
