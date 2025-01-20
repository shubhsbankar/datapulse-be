from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RtDTO(BaseModel):
    tgthashid: int | str | None = None
    projectshortname: str
    tgtdphash: Optional[str] = None
    tgtdataset: str
    datastoreshortname: Optional[str] = None
    tablename: Optional[str] = None
    tgttabfields: Optional[List[str]] = None
    tgthashcol: Optional[str] = None
    dpname: str
    bkeys: Optional[str] = None
    bkey1: Optional[str] = None
    bkey2: Optional[str] = None
    bkey3: Optional[str] = None
    bkey4: Optional[str] = None
    bkey5: Optional[str] = None
    bkey6: Optional[str] = None
    bkey7: Optional[str] = None
    bkey8: Optional[str] = None
    bkey9: Optional[str] = None
    bkey10: Optional[str] = None
    createdate: str | None = None

    class Config:
        from_attributes = True
