from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.rdvbojds_dto import RdvBojDsDTO

router = APIRouter()

from .rdvbojdsGet import get_all_rdvbojds
from .rdvbojdsPost import create_rdvbojds, test_rdvbojds
from .rdvbojdsPut import update_rdvbojds
