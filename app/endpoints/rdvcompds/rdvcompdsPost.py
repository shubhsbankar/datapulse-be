from app.db import get_db, get_sqlalchemy_conn

import pandas as pd
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.endpoints.rdvcompds import (
    router,
    auth_dependency,
    get_db,
    response,
    RdvCompDsDTO,
)

@router.post("/get-columns")
async def get_table_columns(data: dict, current_user: dict = Depends(auth_dependency)):
    print(data)
    
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # Use pandas to get column information
            query = f"SELECT * FROM tst1a.datasets"
            df = pd.read_sql(query, conn)
            columns = df.columns.tolist()

            return response(200, "Columns fetched successfully", data=columns)
    except Exception as e:
        return response(400, str(e))



@router.post("/create")
async def create_rdvcompds(
    rdvcompds: RdvCompDsDTO, current_user: dict = Depends(auth_dependency)
):
    print(rdvcompds)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.rdvcompds (
                    projectshortname, dpname, dsname, comptype,
                    satlname, satlattr, assoccomptype, assoccompname,
                    tenantid, bkcarea, user_email, compshortname,
                    version, partsnum, parts
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    rdvcompds.projectshortname,
                    rdvcompds.dpname,
                    rdvcompds.dsname,
                    rdvcompds.comptype,
                    rdvcompds.compshortname,
                    # rdvcompds.satlname,
                    rdvcompds.satlattr,
                    rdvcompds.assoccomptype,
                    rdvcompds.assoccompname,
                    rdvcompds.tenantid,
                    rdvcompds.bkcarea,
                    current_user["sub"],
                    # rdvcompds.compshortname, - >> compshortname is incorrect, its the concat of projectshortname, dpname, dsname, satlname, version
                    f"{rdvcompds.projectshortname}_{rdvcompds.dpname}_{rdvcompds.dsname}_{rdvcompds.compshortname}_{int(rdvcompds.version)}",
                    rdvcompds.version,
                    rdvcompds.partsnum,
                    rdvcompds.parts,
                ),
            )
            conn.commit()

            return response(201, "RdvCompDs created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_rdvcompds(
    rdvcompds: RdvCompDsDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in rdvcompds.dict().items():
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

        # print("\n\nTest successful: RdvCompDs configuration is valid\n\n")
        # return response(200, "RdvCompDs test successful")

    except Exception as e:
        return response(400, str(e))
