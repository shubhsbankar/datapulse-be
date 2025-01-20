import datetime
from fastapi.params import Query
from app.endpoints.filemanagment import *


# BigQuery Files
@router.post("/bigquery/upload")
async def upload_bigquery_files(
    project_shortname: str = Form(...), files: List[UploadFile] = File(...)
):
    try:
        paths = get_project_paths(project_shortname)
        bigquery_path = paths["BIGQUERY_FILES"]
        os.makedirs(bigquery_path, exist_ok=True)

        saved_files = []
        for file in files:
            file_path = os.path.join(bigquery_path, file.filename)
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            saved_files.append(file_path)

        return response(200, "Files uploaded successfully", {"files": saved_files})
    except Exception as e:
        return response(400, str(e))


# CDS Files
@router.post("/cds/upload")
async def upload_cds_files(
    project_shortname: str = Form(...), files: List[UploadFile] = File(...)
):
    try:
        paths = get_project_paths(project_shortname)
        cds_path = paths["CDS_FILES"]
        os.makedirs(cds_path, exist_ok=True)

        saved_files = []
        for file in files:
            file_path = os.path.join(cds_path, file.filename)
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            saved_files.append(file_path)

        return response(200, "Files uploaded successfully", {"files": saved_files})
    except Exception as e:
        return response(400, str(e))


# CDS Credentials
@router.post("/cds/credentials")
async def upload_cds_credentials(
    project_shortname: str = Form(...),
    s3_credentials: UploadFile = File(None),
    gcs_credentials: UploadFile = File(None),
):
    try:
        paths = get_project_paths(project_shortname)
        cds_path = paths["CDS_FILES"]
        os.makedirs(cds_path, exist_ok=True)

        saved_files = []
        if s3_credentials:
            s3_path = os.path.join(cds_path, s3_credentials.filename)
            contents = await s3_credentials.read()
            with open(s3_path, "wb") as f:
                f.write(contents)
            saved_files.append(s3_path)

        if gcs_credentials:
            gcs_path = os.path.join(cds_path, gcs_credentials.filename)
            contents = await gcs_credentials.read()
            with open(gcs_path, "wb") as f:
                f.write(contents)
            saved_files.append(gcs_path)

        return response(200, "Credentials saved successfully", {"files": saved_files})
    except Exception as e:
        return response(400, str(e))


# DT Files
@router.post("/dt/upload")
async def upload_dt_files(
    project_shortname: str = Form(...), files: List[UploadFile] = File(...)
):
    try:
        paths = get_project_paths(project_shortname)
        dt_path = paths["DT_FILES"]
        os.makedirs(dt_path, exist_ok=True)

        saved_files = []
        for file in files:
            file_path = os.path.join(dt_path, file.filename)
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            saved_files.append(file_path)

        return response(200, "Files uploaded successfully", {"files": saved_files})
    except Exception as e:
        return response(400, str(e))


# Python Files
@router.post("/python-files/upload")
async def upload_python_files(
    files: List[UploadFile] = File(...),
    filetype: str = Query(...),
    project_id: str = Query(None),
):
    try:
        if filetype:
            paths = get_python_file_paths(project_id, filetype)
            py_path = paths["UPLOAD_PATH"]
        else:
            paths = get_project_paths(project_id)
            py_path = paths["PYTHON_FILES"]
        
        print(f"py_path: {py_path}")
        os.makedirs(py_path, exist_ok=True)
        saved_files = []
        for file in files:
            if not file.filename.endswith(".py"):
                continue
            file_path = os.path.join(py_path, file.filename)
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            saved_files.append(file_path)

        return response(200, "Files uploaded successfully", {"files": saved_files})
    except PermissionError:
        return response(400, f"Permission denied for directory: {py_path}")
    except FileNotFoundError:
        return response(400, f"Base directory missing: {os.path.dirname(py_path)}")
    except Exception as e:
        print(e)
        return response(400, str(e))


# CSV Files
@router.post("/csv/upload")
async def upload_csv_files(
    project_shortname: str = Form(...),
    files: List[UploadFile] = File(...),
    timestamp: str = Form(None),
):
    try:
        if not timestamp:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        paths = get_project_paths(project_shortname)
        csv_path = os.path.join(paths["CSV_FILES"], timestamp)
        os.makedirs(csv_path, exist_ok=True)

        print(f"CSV Files: {[f.filename for f in files]}")
        print(f"Folder Path: {csv_path}")
        print(f"Project Shortname: {project_shortname}")
        print(f"Table Name: {timestamp}")

        saved_files = []
        for file in files:
            file_path = os.path.join(csv_path, file.filename)
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            saved_files.append(file_path)

        return response(
            200,
            "Files uploaded successfully",
            {"files": saved_files, "timestamp": timestamp, "path": csv_path},
        )
    except Exception as e:
        return response(400, str(e))


# YAML Files
@router.post("/yaml/upload")
async def upload_yaml_files(
    project_shortname: str = Form(...), files: List[UploadFile] = File(...)
):
    try:
        paths = get_project_paths(project_shortname)
        yaml_path = paths["YAML_FILES"]
        os.makedirs(yaml_path, exist_ok=True)

        saved_files = []
        for file in files:
            file_path = os.path.join(yaml_path, file.filename)
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            saved_files.append(file_path)

        return response(200, "Files uploaded successfully", {"files": saved_files})
    except Exception as e:
        return response(400, str(e))
