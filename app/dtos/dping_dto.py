from pydantic import BaseModel


class Dping(BaseModel):
    dpid: int | None = None
    dpshortname: str | None = None
    htmlfilename: str | None = None
    datasettype: str | None = None
    projectshortname: str | None = None
    datasetshortname: str | None = None
    dataproductshortname: str | None = None
    createdate: str | None = None
    useremailid: str | None = None
