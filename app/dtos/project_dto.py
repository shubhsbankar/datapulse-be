from pydantic import BaseModel


class ProjectBase(BaseModel):
    projectshortname: str
    projectname: str
    coname: str
    datastoreshortname: str


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
