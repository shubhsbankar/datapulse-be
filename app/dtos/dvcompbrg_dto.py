from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DvCompBrgDTO(BaseModel):
    dvid: int | str | None = None
    projectshortname: str
    comptype: str
    compname: str
    compsubtype: str
    sqltext: Optional[str] = None
    createdate: str | None = None
    compshortname: Optional[str] = None
    comments: Optional[str] = None
    version: Optional[float] = None
    processtype: Optional[str] = None
    datefieldname: Optional[str] = None
    hubnums: Optional[int] = None
    hubnum: Optional[int] = None
    hubname: str | None = None
    hubversion: Optional[float] = None
    bkfields: Optional[List[str]] = None 
    lnknums: Optional[int] = None
    lnknum: Optional[int] = None
    lnkname: str | None = None
    lnkversion: Optional[float] = None
    lnkbkfields: Optional[List[str]] = None

    class Config:
        from_attributes = True
