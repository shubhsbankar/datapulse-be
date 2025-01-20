from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import pandas as pd
from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db, get_sqlalchemy_conn
from app.dtos.dtg_dto import DtgDTO, SqlExecuteDTO

router = APIRouter()

from .dtgGet import get_all_dtgs
from .dtgPost import create_dtg, test_dtg
from .dtgPut import update_dtg
