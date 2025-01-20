from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.rdvcompds_dto import RdvCompDsDTO

router = APIRouter()

from .rdvcompdsGet import get_all_rdvcompds
from .rdvcompdsPost import create_rdvcompds, test_rdvcompds, get_table_columns
from .rdvcompdsPut import update_rdvcompds
