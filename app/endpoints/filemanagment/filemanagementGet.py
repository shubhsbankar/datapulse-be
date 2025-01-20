import random
from fastapi.params import Query
import pandas as pd
from app.endpoints.filemanagment import *
from fastapi.responses import FileResponse
import shutil
from datetime import datetime
from app.utils.constants import BASE_PATH, TMP_PATH
import glob
import tempfile
import zipfile


@router.get("/cds/download/{project_id}")
async def download_cds_files(project_id: str):
    try:
        paths = get_project_paths(project_id)
        cds_path = paths["CDS_FILES"]

        if not os.path.exists(cds_path):
            return response(404, "No files found")

        # Create a temporary zip file
        zip_filename = f"cds_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join("/tmp", zip_filename)

        # Create zip archive
        shutil.make_archive(zip_path[:-4], "zip", cds_path)

        return FileResponse(
            zip_path, media_type="application/zip", filename=zip_filename
        )
    except Exception as e:
        return response(400, str(e))


@router.get("/dping/download/{project_id}/{filename}")
async def download_dping_files(project_id: str, filename: str):
    paths = get_project_paths(project_id)
    dping_path = paths["DPING_DOWNLOAD_PATH"]

    if not os.path.exists(dping_path):
        return response(400, "No file found")

    file_path = os.path.join(dping_path, filename)
    if not os.path.exists(file_path):
        return response(400, "File not found")

    return FileResponse(file_path)


@router.get("/dt/download/{project_id}")
async def download_dt_files(project_id: str):
    try:
        paths = get_project_paths(project_id)
        dt_path = paths["DT_FILES"]

        if not os.path.exists(dt_path):
            return response(404, "No files found")

        zip_filename = f"dt_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join("/tmp", zip_filename)

        shutil.make_archive(zip_path[:-4], "zip", dt_path)

        return FileResponse(
            zip_path, media_type="application/zip", filename=zip_filename
        )
    except Exception as e:
        return response(400, str(e))


@router.get("/python-files/download")
async def download_python_files(
    project_id: str = Query(None), filetype: str = Query(None), filepath: str = Query(None)
):
    
    try:
        if project_id:
            paths = get_project_paths(project_id)
            py_path = paths["PYTHON_FILES"]
        else:
            paths = get_python_file_paths("", filetype)
            py_path = paths["DOWNLOAD_PATH"]
    
        print(f"py_path: {py_path}")        
        if filetype:
            py_path = f"{py_path}/{filetype}"
            
        if filepath:
            py_path = f"{py_path}/{filepath}"
            if not os.path.exists(py_path):
                print("No files found")
                return response(404, "No files found")    
            return FileResponse(py_path, media_type="application/py", filename=filepath)
            
        # print(f"py_path: {py_path}")

        # if not os.path.exists(py_path):
        #     print("No files found")
        #     return response(400, "No files found")

        zip_filename = f"python_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join("/tmp", zip_filename)

        # shutil.make_archive(zip_path[:-4], "zip", py_path)

        # return FileResponse(
        #     zip_path, media_type="application/zip", filename=zip_filename
        # )
        
        
        # Temporary directory to store the zip file
        with tempfile.TemporaryDirectory() as temp_dir:
            # Path to the zip file
            # zip_file_path = os.path.join(temp_dir, "files.zip")
            # Create a zip file
            with zipfile.ZipFile(zip_path, "w") as zipf:
                # Define the search pattern
                search_pattern = os.path.join(BASE_PATH, "*", "file-uploads", "python_files", filetype,f"*-{filetype}-*.py")
                print(search_pattern)
                # Find all matching files
                matching_files = glob.glob(search_pattern)
                if not matching_files:
                    return response(404, "No files found.")
                # Add each file to the zip archive
                for file_path in matching_files:
                    # Include file's relative path in the archive
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname)
            # Serve the zip file as a response
            return FileResponse(zip_path, filename=zip_filename, media_type="application/zip")
    except Exception as e:
        return response(400, str(e))


@router.get("/python-files/download-hardcoded")
async def download_python_files(
    filepath: str = Query(None)
):
    try:
        if not filepath:
            return response(400, "Please provide filepath")
        
        py_path = get_predefind_files_path()
        py_path = os.path.join(py_path, filepath)
        if not os.path.exists(py_path):
            print("No files found")
            return response(404, "No files found")    
        return FileResponse(py_path, media_type="application/py", filename=filepath)
            
    except Exception as e:
        return response(400, str(e))

@router.get("/python-files/download-predefined")
async def download_python_files():
    try:
        py_path = get_predefind_files_path()
        if not os.path.exists(py_path):
            print("No files found")
            return response(404, "No files found")    
        
        zip_filename = f"python_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join("/tmp", zip_filename)

        shutil.make_archive(zip_path[:-4], "zip", py_path)

        return FileResponse(
            zip_path, media_type="application/zip", filename=zip_filename
        )
    except Exception as e:
        print(e)
        return response(400, str(e))


@router.get("/csv/download/{project_id}")
async def download_csv_files(
    project_id: str,
    timestamp: str,
    table: str,
    current_user: dict = Depends(auth_dependency),
):
    try:
        paths = get_project_paths(project_id)
        csv_path = os.path.join(paths["CSV_FILES"], timestamp)

        if not os.path.exists(csv_path):
            return response(404, "No files found")

        # Filter files by table name if provided
        files = [f for f in os.listdir(csv_path) if f.startswith(table)]
        if not files:
            return response(404, "No matching files found")

        zip_filename = (
            f"{table}_csv_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        )
        zip_path = os.path.join("/tmp", zip_filename)

        # Create zip with only matching files
        with shutil.ZipFile(zip_path, "w") as zipf:
            for file in files:
                file_path = os.path.join(csv_path, file)
                zipf.write(file_path, file)

        return FileResponse(
            zip_path, media_type="application/zip", filename=zip_filename
        )
    except Exception as e:
        return response(400, str(e))


@router.get("/csv/all/download/{project_id}/{timestamp}")
async def download_csv_files(
    project_id: str,
    timestamp: str,
):
    try:
        tables = [
            "projects",
            "datastores",
            "datasets",
            "dping",
            "dtg",
            "rs",
            "rt",
            "str",
            "tenantbkcc",
            "rdvcompdh",
            "rdvcompds",
            "rdvcompdl",
            "rdvbojds",
            "dvcompsg1",
            "dvbojsg1",
        ]
        # Filter files by table name if provided
        files = []
        with get_db() as (conn, cursor):
            path = TMP_PATH + str(random.randint(1, 1000000))
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

            for table in tables:
                try:
                    query = f"SELECT * FROM tst1a.{table} WHERE createdate >= %s and projectshortname = %s"
                    df = pd.read_sql_query(query, conn, params=(timestamp, project_id,))
                except Exception as e:
                    query = f"SELECT * FROM tst1a.{table} WHERE createdate >= %s"
                    df = pd.read_sql_query(query, conn, params=(timestamp,))
                df.to_csv(
                    os.path.join(path, f"{table}.csv"),
                    index=False,
                )
                files.append(f"{table}.csv")
        if not files:
            return response(404, "No matching files found")

        zip_filename = f"csv_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join("/tmp", zip_filename)

        # Create zip archive of files
        shutil.make_archive(zip_path[:-4], "zip", path)

        return FileResponse(
            zip_path, media_type="application/zip", filename=zip_filename
        )
    except Exception as e:
        return response(400, str(e))


@router.get("/yaml/download/{project_id}")
async def download_yaml_files(project_id: str, filename: str = Query(None)):
    try:
        paths = get_project_paths(project_id)
        yaml_path = paths["YAML_FILES"]
        
        if filename:
            yaml_path = f"{yaml_path}/{filename}"
            if not os.path.exists(yaml_path):
                return response(404, "No files found")
            return FileResponse(yaml_path, media_type="application/yaml", filename=filename)

        if not os.path.exists(yaml_path):
            return response(404, "No files found")

        zip_filename = f"yaml_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join("/tmp", zip_filename)

        shutil.make_archive(zip_path[:-4], "zip", yaml_path)

        return FileResponse(
            zip_path, media_type="application/zip", filename=zip_filename
        )
    except Exception as e:
        return response(400, str(e))


# Clean up function to remove temporary zip files
def cleanup_temp_files(zip_path: str):
    try:
        if os.path.exists(zip_path):
            os.remove(zip_path)
    except Exception as e:
        print(f"Error cleaning up temp file {zip_path}: {str(e)}")
