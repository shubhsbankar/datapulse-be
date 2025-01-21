from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DvCompSg2DTO(BaseModel):
    dvid: int | str | None = None
    projectshortname: str
    comptype: str
    compname: str
    compsubtype: str
    sqltext: Optional[str] = None
    createdate: str | None = None
    compshortname: Optional[str] = None
    user_email: Optional[str] = None
    comments: Optional[str] = None
    version: Optional[float] = None

    class Config:
        from_attributes = True
