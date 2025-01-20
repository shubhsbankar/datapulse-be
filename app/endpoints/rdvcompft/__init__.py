import pandas as pd

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db, get_sqlalchemy_conn
from app.dtos.rdvcompft_dto import RdvCompFtDTO

router = APIRouter()

from .rdvcompftGet import get_all_rdvcompft
from .rdvcompftPost import create_rdvcompft, test_rdvcompft, get_table_columns
from .rdvcompftPut import update_rdvcompft
