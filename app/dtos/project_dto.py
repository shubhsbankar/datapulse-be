from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SourceType(str, Enum):
    GCS = "GCS"
    AWS_S3 = "AWSS3"
    Local = "Local"


class ProjectBase(BaseModel):
    projectshortname: str
    projectname: str
    coname: str
    datastoreshortname: str
    sourcetype: SourceType
    credentials_file: Optional[str] = None  # For GCS, null if not provided
    accesskey: Optional[str] = None       # For AWS S3, null if not provided  
    secretkey: Optional[str] = None       # For AWS S3, null if not provided


class Project(ProjectBase):
    projectid: int
    createdate: str
    user_email: str


class ProjectAssignBase(BaseModel):
    useremail: str
    projectshortname: str
    is_active: bool


class ProjectAssign(ProjectAssignBase):
    assignid: int
    createdate: str
    who_added: str


class ProjectAssignUpdate(BaseModel):
    is_active: bool
