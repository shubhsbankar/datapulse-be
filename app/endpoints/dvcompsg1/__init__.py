from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.dvcompsg1_dto import DvCompSg1DTO

router = APIRouter()

from .dvcompsg1Get import get_all_dvcompsg1s
from .dvcompsg1Post import create_dvcompsg1, test_dvcompsg1
from .dvcompsg1Put import update_dvcompsg1
