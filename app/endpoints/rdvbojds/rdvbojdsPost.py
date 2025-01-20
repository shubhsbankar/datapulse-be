from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvbojds import (
    router,
    auth_dependency,
    get_db,
    response,
    RdvBojDsDTO,
)
from app.db import get_sqlalchemy_conn
from fastapi.encoders import jsonable_encoder
import pandas as pd

@router.post("/create")
async def create_rdvbojds(
    rdvbojds: RdvBojDsDTO, current_user: dict = Depends(auth_dependency)
):
    print(rdvbojds)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.rdvbojds (
                    projectshortname, dpname, dsname, comptype,
                    compname, satlnums, satlnum, satlname,
                    satlversion, tenantid, bkcarea, compshortname,
                    user_email, comments, version
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    rdvbojds.projectshortname,
                    rdvbojds.dpname,
                    rdvbojds.dsname,
                    rdvbojds.comptype,
                    rdvbojds.compname,
                    rdvbojds.satlnums,
                    rdvbojds.satlnum,
                    rdvbojds.satlname,
                    rdvbojds.satlversion,
                    rdvbojds.tenantid,
                    rdvbojds.bkcarea,
                    rdvbojds.compshortname,
                    current_user["sub"],
                    rdvbojds.comments,
                    rdvbojds.version,
                ),
            )
            conn.commit()

            return response(201, "RdvBojDs created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_rdvbojds(
    rdvbojds: RdvBojDsDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in rdvbojds.dict().items():
            if value is not None:
                print(f"{field}: {value}")


        filter_query = f"SELECT * FROM tst1a.users_latest"
        conn = get_sqlalchemy_conn()
        df = pd.read_sql(filter_query, conn)
        print(df)
        if df.empty:
            return response(404, "Dataset not found.")
        conn.commit()

        headers = jsonable_encoder(df.columns.tolist())
        rows = jsonable_encoder(df.values.tolist())
        if df.empty:
            return response(404, "Dataset not found.")
        conn.commit()
        return response(
            200, "Test connection successful!", data={"headers": headers, "rows": rows}
        )

        # print("\n\nTest successful: RdvBojDs configuration is valid\n\n")
        # return response(200, "RdvBojDs test successful")

    except Exception as e:
        return response(400, str(e))
