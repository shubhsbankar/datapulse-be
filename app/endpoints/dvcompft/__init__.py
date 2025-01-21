import pandas as pd

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db, get_sqlalchemy_conn
from app.dtos.dvcompft_dto import DvCompFtDTO

router = APIRouter()

from .dvcompftGet import get_all_dvcompft
from .dvcompftPost import create_dvcompft, test_dvcompft, get_table_columns
from .dvcompftPut import update_dvcompft
