from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RdvBojDsDTO(BaseModel):
    rdvid: int | str | None = None
    projectshortname: str
    dpname: Optional[str] = None
    dsname: str
    comptype: Optional[str] = None
    compname: str
    satlnums: Optional[int] = None
    satlnum: Optional[int] = None
    satlname: Optional[str] = ""
    satlversion: Optional[float] = None
    tenantid: str
    bkcarea: str
    createdate: str | None = None
    compshortname: str | None = None
    user_email: str | None = None
    comments: str | None = None
    version: float | None = None

    class Config:
        from_attributes = True
