import dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints.auth import router as auth_router
from app.endpoints.user import router as user_router
from app.endpoints.project import router as project_router
from app.endpoints.datastore import router as datastore_router
from app.endpoints.dataset import router as dataset_router
from app.endpoints.dping import router as dping_router
from app.endpoints.dtg import router as dtg_router
from app.endpoints.dvbojsg1 import router as dvbojsg1_router
from app.endpoints.dvcompsg1 import router as dvcompsg1_router
from app.endpoints.dvcompsg1b import router as dvcompsg1b_router
from app.endpoints.rdvbojds import router as rdvbojds_router
from app.endpoints.rdvcompdh import router as rdvcompdh_router
from app.endpoints.rdvcompdl import router as rdvcompdl_router
from app.endpoints.rdvcompds import router as rdvcompds_router
from app.endpoints.dvcomppt import router as dvcomppt_router
from app.endpoints.dvcompbrg import router as dvcompbrg_router
from app.endpoints.dvcompbrg2 import router as dvcompbrg2_router
from app.endpoints.rs import router as rs_router
from app.endpoints.rt import router as rt_router
from app.endpoints.str import router as str_router
from app.endpoints.tenantbkcc import router as tenantbkcc_router
from app.endpoints.filemanagment import router as filemanagment_router
from app.endpoints.adhoc import router as adhoc_router
from app.endpoints.dvcompsg2 import router as dvcompsg2_router
from app.endpoints.dvcompdd import router as dvcompdd_router
from app.endpoints.dvcompft import router as dvcompft_router
from app.endpoints.landingdataset import router as landingdataset_router
import app.db as db_init

dotenv.load_dotenv()

origins = ["*"]

# FastAPI app and JWT secret
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(project_router, prefix="/project")
app.include_router(datastore_router, prefix="/datastore")
app.include_router(dataset_router, prefix="/dataset")
app.include_router(dping_router, prefix="/dping")
app.include_router(dtg_router, prefix="/dtg")
app.include_router(dvbojsg1_router, prefix="/dvbojsg1")
app.include_router(dvcompsg1_router, prefix="/dvcompsg1")
app.include_router(dvcompsg1b_router, prefix="/dvcompsg1b")
app.include_router(rdvbojds_router, prefix="/rdvbojds")
app.include_router(rdvcompdh_router, prefix="/rdvcompdh")
app.include_router(rdvcompdl_router, prefix="/rdvcompdl")
app.include_router(rdvcompds_router, prefix="/rdvcompds")
app.include_router(rs_router, prefix="/rs")
app.include_router(rt_router, prefix="/rt")
app.include_router(str_router, prefix="/str")
app.include_router(tenantbkcc_router, prefix="/tenantbkcc")
app.include_router(filemanagment_router, prefix="/filemanagment")
app.include_router(adhoc_router, prefix="/adhoc")
app.include_router(dvcomppt_router, prefix="/dvcomppt")
app.include_router(dvcompbrg_router, prefix="/dvcompbrg")
app.include_router(dvcompbrg2_router, prefix="/dvcompbrg2")
app.include_router(dvcompsg2_router, prefix="/dvcompsg2")
app.include_router(dvcompdd_router, prefix="/dvcompdd")
app.include_router(dvcompft_router, prefix="/dvcompft")
app.include_router(landingdataset_router, prefix="/landingdataset")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
