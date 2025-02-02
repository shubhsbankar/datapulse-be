from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LandingDataset(BaseModel):
    dlid: int | str | None = None
    projectshortname: str | None = None
    srcdataproductshortname: str | None = None
    srcdatasetshortname: str | None = None
    lnddataproductshortname: str | None = None
    lnddatasetshortname: str | None = None
    lnddsshortname: str | None = None
    createdate: str | None = None
    useremailid: str | None = None
    comments: str | None = None