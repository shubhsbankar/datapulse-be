from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.dping_dto import Dping

router = APIRouter()

from .dpingGet import get_all_dpings
from .dpingPost import create_dping, test_dping
from .dpingPut import update_dping
