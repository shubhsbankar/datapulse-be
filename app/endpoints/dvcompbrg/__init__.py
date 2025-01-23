from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.dvcompbrg_dto import DvCompBrgDTO

router = APIRouter()

from .dvcompbrgPost import test_dvcompbrg, create_dvcompbrg, get_table_columns
from .dvcompbrgGet import get_all_dvcompbrgs
from .dvcompbrgPut import update_dvcompbrg