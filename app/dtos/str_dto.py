from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StrDTO(BaseModel):
    # srctgthashid: Optional[int]
    projectshortname: str
    srctgthash: str
    srchash: Optional[str]
    tgthash: Optional[str]
    rtype: Optional[str]
    rdata: Optional[str]
    rfield: Optional[str]
    hr_exec: Optional[str]
    createdate: datetime
    rtbkeys: Optional[str]
    rsbkeys: Optional[str]

    class Config:
        from_attributes = True
