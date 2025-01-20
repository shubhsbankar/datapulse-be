from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import pandas as pd
from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.rt_dto import RtDTO

router = APIRouter()

from .rtGet import get_all_rt
from .rtPost import create_rt, test_rt, get_table_columns, get_table_names
from .rtPut import update_rt
