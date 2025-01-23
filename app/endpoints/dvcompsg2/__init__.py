from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.dvcompsg2_dto import DvCompSg2DTO

router = APIRouter()

from .dvcompsg2Get import get_all_dvcompsg2s
from .dvcompsg2Post import create_dvcompsg2, test_dvcompsg2, get_table_columns
from .dvcompsg2Put import update_dvcompsg2
