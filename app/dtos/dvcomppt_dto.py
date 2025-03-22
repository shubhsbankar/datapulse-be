from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DvCompPtDTO(BaseModel):
    rdvid: int | str | None = None
    projectshortname: str
    comptype: Optional[str] = None
    compname: str
    compsubtype: str
    satlnums: Optional[int] = None
    satlnum: Optional[int] = None
    satlname: Optional[str] = ""
    satlversion: Optional[float] = None
    createdate: str | None = None
    compshortname: str | None = None
    comments: str | None = None
    version: float | None = None
    dhname: str | None = None
    dlname: str | None = None
    user_email: Optional[str] = None

    class Config:
        from_attributes = True
