from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.dvcomppt_dto import DvCompPtDTO

router = APIRouter()

from .dvcompptPost import test_dvcomppt, create_dvcomppt
from .dvcompptGet import get_all_dvcomppts
from .dvcompptPut import update_dvcomppt