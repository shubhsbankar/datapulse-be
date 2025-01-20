from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RdvCompDlDTO(BaseModel):
    rdvid: int | None = None
    projectshortname: str
    dpname: Optional[str] = None
    dsname: str
    comptype: Optional[str] = None
    compname: str
    compkeyname: str
    hubnums: Optional[int] = None
    hubnum: Optional[int] = None
    hubname: str | None = None
    hubversion: Optional[float] = None
    bkfields: Optional[List[str]] = None
    degen: Optional[str] = None
    degenids: Optional[List[str]] = None
    tenantid: str | None = None
    bkcarea: str | None = None
    createdate: str | None = None
    user_email: Optional[str] = None
    compshortname: Optional[str] = None
    version: Optional[float] = None

    class Config:
        from_attributes = True
