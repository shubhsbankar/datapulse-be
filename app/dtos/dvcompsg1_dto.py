from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DvCompSg1DTO(BaseModel):
    rdvid: int | str | None = None
    projectshortname: str
    dpname: Optional[str] = None
    dsname: Optional[str] = None
    comptype: str
    compname: str
    compsubtype: str
    sqltext: Optional[str] = None
    tenantid: Optional[str] = None
    bkcarea: Optional[str] = None
    createdate: str | None = None
    compshortname: Optional[str] = None
    user_email: Optional[str] = None
    comments: Optional[str] = None
    version: Optional[float] = None
    processtype: Optional[str] = None
    datefieldname: Optional[str] = None
    partsnum: Optional[int] = None
    parts: Optional[List[str]] = None

    class Config:
        from_attributes = True
