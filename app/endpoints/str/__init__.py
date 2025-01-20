from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.str_dto import StrDTO

router = APIRouter()

from .strGet import get_all_str
from .strPost import create_str, test_str
from .strPut import update_str
