from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.db import get_db
from app.dtos.tenantbkcc_dto import TenantBkccDTO

router = APIRouter()

from .tenantbkccGet import get_all_tenantbkcc
from .tenantbkccPost import create_tenantbkcc, test_tenantbkcc
from .tenantbkccPut import update_tenantbkcc
