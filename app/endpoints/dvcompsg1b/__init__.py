from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.dvcompsg1b_dto import DvCompSg1DTO

router = APIRouter()

from .dvcompsg1bGet import get_all_dvcompsg1bs
from .dvcompsg1bPost import create_dvcompsg1b, test_dvcompsg1b
from .dvcompsg1bPut import update_dvcompsg1b
