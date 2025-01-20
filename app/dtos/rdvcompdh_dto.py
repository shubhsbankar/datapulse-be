from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RdvCompDhDTO(BaseModel):
    rdvid: int | None = None
    projectshortname: str
    dpname: Optional[str]
    dsname: str
    comptype: Optional[str]
    compname: str
    compkeyname: str
    bkfields: List[str]
    tenantid: Optional[str] | None = None
    bkcarea: Optional[str] | None = None
    createdate: str | None = None
    compshortname: Optional[str] | None = None
    user_email: Optional[str] | None = None
    version: Optional[float] | None = None

    class Config:
        from_attributes = True
