from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Dataset(BaseModel):
    datasetid: int | str | None = None
    datasettype: str | None = None
    csvname: str | None = None
    tablename: str | None = None
    csvdailysuffix: str | None = None
    datasetshortname: str | None = None
    datastoreshortname: str | None = None
    dataproductshortname: str | None = None
    projectshortname: str | None = None
    domainshortname: str | None = None
    separator: str | None = None
    createdate: str | None = None
    dsdatatype: str | None = None
    fieldname: str | None = None
    is_valid: bool | str | None = None
    useremailid: str | None = None
    sourcename: str | None = None
    tenantid: str | None = None
    bkcarea: str | None = None
    filessource: str | None = None
    filesbucketpath: str | None = None
    s3_accesskey: str | None = None
    s3_secretkey: str | None = None
    gcs_jsonfile: str | None = None
