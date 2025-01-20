import pandas as pd
from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvbojsg1 import (
    router,
    auth_dependency,
    get_db,
    response,
    DvBojSg1DTO,
)
from app.db import get_sqlalchemy_conn
from fastapi.encoders import jsonable_encoder


@router.post("/create")
async def create_dvbojsg1(
    dvbojsg1: DvBojSg1DTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.dvbojsg1 (
                    projectshortname, dpname, dsname, comptype,
                    compname, compsubtype, sqltext, tenantid,
                    bkcarea, compshortname, user_email, comments,
                    version, processtype, datefieldname, partsnum, parts
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    dvbojsg1.projectshortname,
                    dvbojsg1.dpname,
                    dvbojsg1.dsname,
                    dvbojsg1.comptype,
                    dvbojsg1.compname,
                    dvbojsg1.compsubtype,
                    dvbojsg1.sqltext,
                    dvbojsg1.tenantid,
                    dvbojsg1.bkcarea,
                    dvbojsg1.compshortname,
                    current_user["sub"],
                    dvbojsg1.comments,
                    dvbojsg1.version,
                    dvbojsg1.processtype,
                    dvbojsg1.datefieldname,
                    dvbojsg1.partsnum,
                    dvbojsg1.parts,
                ),
            )
            conn.commit()

            return response(201, "DvBojSg1 created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_dvbojsg1(
    dvbojsg1: DvBojSg1DTO, current_user: dict = Depends(auth_dependency)
):
    print(dvbojsg1)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in dvbojsg1.dict().items():
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
        # return response(
        #     200, "Test connection successful!", data={"error": "Gahalat sql likhi hai"}
        # )
        return response(
            200, "Test connection successful!", data={"headers": headers, "rows": rows}
        )

        # print("\n\nTest successful: DvBojSg1 configuration is valid\n\n")
        # return response(200, "DvBojSg1 test successful")

    except Exception as e:
        return response(400, str(e))
    
@router.post("/columns")
async def get_dvbojsg1_columns():
    try:
        filter_query = f"SELECT * FROM tst1a.datastores"
        conn = get_sqlalchemy_conn()
        df = pd.read_sql(filter_query, conn)
        if df.empty:
            return response(404, "Dataset not found.")
        conn.commit()

        headers = jsonable_encoder(df.columns.tolist())
        return response(200, "Columns fetched successfully", data=headers)

    except Exception as e:
        return response(400, str(e))
