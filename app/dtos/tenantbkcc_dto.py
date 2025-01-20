from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TenantBkccDTO(BaseModel):
    tenantid: str | None = None
    bkcarea: str
    hubname: str
    bkcc: str | None = None
    createdate: str | None = None
    user_email: str | None = None

    class Config:
        from_attributes = True
