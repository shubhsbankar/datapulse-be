from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DvCompDdDTO(BaseModel):
    dvid: int | None = None
    projectshortname: str
    comptype: Optional[str]
    compname: str
    compsubtype: str
    bkfields: List[str]
    createdate: str | None = None
    compshortname: Optional[str] | None = None
    version: Optional[float] | None = None
    comments: str | None = None
    datefieldname: Optional[str] = None
    sqltext: Optional[str] = None
    user_email: Optional[str] = None
    

    class Config:
        from_attributes = True
