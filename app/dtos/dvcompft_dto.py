from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DvCompFtDTO(BaseModel):
    rdvid: int | None = None
    projectshortname: str
    comptype: Optional[str]
    compname: str
    compsubtype: str
    # createdate: str | None = None
    compshortname: Optional[str] | None = None
    version: Optional[float] | None = None
    comments: str | None = None
    datefieldname: Optional[str] = None
    sqltext: Optional[str] = None
    ddnums: Optional[int] = None
    ddnum: Optional[int] = None
    ddname: str | None = None
    ddversion: Optional[float] = None
    bkfields: Optional[List[str]] = None
    

    class Config:
        from_attributes = True
