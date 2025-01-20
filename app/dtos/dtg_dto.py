from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DtgDTO(BaseModel):
    dtid: Optional[int] = None
    dtshortname: str
    chkfilename: Optional[str] = None
    datasettype: Optional[str] = None
    datasrcnum: Optional[str] = None
    projectshortname: str
    datasetshortname: str
    dataproductshortname: str
    createdate: Optional[str] = None
    useremailid: Optional[str] = None
    testcoverageversion: Optional[str] = None
    comments: Optional[str] = None

    class Config:
        from_attributes = True


class SqlExecuteDTO(BaseModel):
    dataproductshortname: str
    datasetshortname: str
    projectshortname: str
    sqlQuery: str
    testcoverageversion: str
    executiondate: str
