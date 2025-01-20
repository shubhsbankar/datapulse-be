from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.rs_dto import RsDTO

router = APIRouter()

from .rsGet import get_all_rs
from .rsPost import create_rs, test_rs, get_table_columns
from .rsPut import update_rs
