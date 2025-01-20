import os

# Base path that will be used for all file operations
# BASE_PATH = "/home/f/w/p/yadv"
# TMP_PATH = "/home/f/w/p/yadv/tmp"
BASE_PATH = "/home/abbas/yadv"
TMP_PATH = "/home/abbas/yadv/tmp"


def get_project_paths(projectshortname: str) -> dict:
    """Returns a dictionary of paths for a given project"""
    return {
        "CDS_FILES": os.path.join(BASE_PATH, projectshortname, "file-uploads", "cds"),
        "PREDEFINED_PYTHON_FILES": os.path.join(BASE_PATH, "predefined"), # used in /user/python-files "download predefind files button"
        "BIGQUERY_FILES": os.path.join(
            BASE_PATH, projectshortname, "file-uploads", "big_query"
        ),
        "DPING_DOWNLOAD_PATH": os.path.join(
            BASE_PATH, projectshortname, "file-uploads", "dping"
        ),
        "DT_FILES": os.path.join(BASE_PATH, projectshortname, "file-uploads", "dt"),
        "PYTHON_FILES": os.path.join(
            BASE_PATH, projectshortname, "file-uploads", "python_files"
        ),
        "CSV_FILES": os.path.join(BASE_PATH, projectshortname, "file-uploads", "csv"),
        "YAML_FILES": os.path.join(BASE_PATH, projectshortname, "file-uploads", "yaml"),
        "PROJECT_PY_FILES": os.path.join(
            BASE_PATH, projectshortname, "file-uploads", "project_py_files"
        ),
    }

def get_predefind_files_path():
    return os.path.join(BASE_PATH, "predefined")

def get_python_file_paths(project_id: str, filetype: str) -> dict:
    return {
        "UPLOAD_PATH": os.path.join(
            BASE_PATH, project_id, "file-uploads", "python_files", filetype
        ),
        "DOWNLOAD_PATH": os.path.join(
            BASE_PATH, project_id, "file-uploads", "python_files", filetype
        ),
    }


# For backward compatibility if needed
DEFAULT_PROJECT = "default"
DEFAULT_PATHS = get_project_paths(DEFAULT_PROJECT)
