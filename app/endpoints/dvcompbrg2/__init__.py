from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.dvcompbrg_dto import DvCompBrgDTO

router = APIRouter()

from .dvcompbrg2Post import test_dvcompbrg2, create_dvcompbrg2, get_table_columns
from .dvcompbrg2Get import get_all_dvcompbrg2s
from .dvcompbrg2Put import update_dvcompbrg2