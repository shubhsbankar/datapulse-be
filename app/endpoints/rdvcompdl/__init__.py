from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import pandas as pd
from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.rdvcompdl_dto import RdvCompDlDTO

router = APIRouter()

from .rdvcompdlGet import get_all_rdvcompdl
from .rdvcompdlPost import create_rdvcompdl, test_rdvcompdl, get_dgenids, get_bkfields
from .rdvcompdlPut import update_rdvcompdl
