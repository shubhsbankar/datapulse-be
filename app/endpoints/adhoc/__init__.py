from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List
import os

from app.utils.responses import response
from app.dependencies.auth_dependency import auth_dependency
from app.utils.constants import get_project_paths, get_python_file_paths, TMP_PATH, get_predefind_files_path
from app.db import get_db

router = APIRouter()

# from .filemanagementGet import (
#     download_cds_files,
#     download_dping_files,
#     download_dt_files,
#     download_yaml_files,
#     download_python_files,
#     download_csv_files,
# )
from .adhocPost import (
    execute
)
