import pandas as pd

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db, get_sqlalchemy_conn
from app.dtos.rdvcompdh_dto import RdvCompDhDTO

router = APIRouter()

from .rdvcompdhGet import get_all_rdvcompdh
from .rdvcompdhPost import create_rdvcompdh, test_rdvcompdh, get_table_columns
from .rdvcompdhPut import update_rdvcompdh
