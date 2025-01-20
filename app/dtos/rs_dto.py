from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RsDTO(BaseModel):
    srchashid: int | None = None
    projectshortname: str
    srcdphash: Optional[str] = None
    srcdataset: str
    srctabfields: Optional[List[str]] = None
    srchashcol: Optional[str] = None
    dpname: str
    datastoreshortname: Optional[str] = None
    tablename: Optional[str] = None
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
