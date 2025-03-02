from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RdvCompDsDTO(BaseModel):
    rdvid: int | None = None
    projectshortname: str
    dpname: Optional[str] = None
    dsname: str | None = None
    comptype: Optional[str] = None
    satlname: str | None = None
    satlattr: List[str]
    assoccomptype: str
    assoccompname: str
    tenantid: Optional[str] = None
    bkcarea: Optional[str] = None
    createdate: str | None = None
    user_email: Optional[str] = None
    compshortname: Optional[str] = None
    version: Optional[float] = None
    partsnum: Optional[int] = None
    # parts is supposed to be a list of strings, but it is not defined in the DTO.
    parts: Optional[List[str]] = None
    datefieldname: Optional[str] = None

    class Config:
        from_attributes = True
