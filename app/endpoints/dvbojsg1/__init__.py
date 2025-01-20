from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.dvbojsg1_dto import DvBojSg1DTO

router = APIRouter()

from .dvbojsg1Get import get_all_dvbojsg1s
from .dvbojsg1Post import create_dvbojsg1, test_dvbojsg1
from .dvbojsg1Put import update_dvbojsg1
