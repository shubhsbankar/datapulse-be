from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DvCompSg2DTO(BaseModel):
    rdvid: int | str | None = None
    comptype: str
    compsubtype: str
    createdate: str | None = None
    version: Optional[float] = None

    class Config:
        from_attributes = True
