import pandas as pd

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db, get_sqlalchemy_conn
from app.dtos.rdvcompdd_dto import RdvCompDdDTO

router = APIRouter()

from .rdvcompddGet import get_all_rdvcompdd
from .rdvcompddPost import create_rdvcompdd, test_rdvcompdd, get_table_columns
from .rdvcompddPut import update_rdvcompdd
