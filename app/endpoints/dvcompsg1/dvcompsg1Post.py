from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompsg1 import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompSg1DTO,
)
from fastapi.encoders import jsonable_encoder
from app.db import get_sqlalchemy_conn
import pandas as pd


@router.post("/create")
async def create_dvcompsg1(
    dvcompsg1: DvCompSg1DTO, current_user: dict = Depends(auth_dependency)
):
    print(dvcompsg1)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.dvcompsg1 (
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
                    dvcompsg1.projectshortname,
                    dvcompsg1.dpname,
                    dvcompsg1.dsname,
                    dvcompsg1.comptype,
                    dvcompsg1.compname,
                    dvcompsg1.compsubtype,
                    dvcompsg1.sqltext,
                    dvcompsg1.tenantid,
                    dvcompsg1.bkcarea,
                    dvcompsg1.compshortname,
                    current_user["sub"],
                    dvcompsg1.comments,
                    dvcompsg1.version,
                    dvcompsg1.processtype,
                    dvcompsg1.datefieldname,
                    dvcompsg1.partsnum,
                    dvcompsg1.parts,
                ),
            )
            conn.commit()

            return response(201, "DvCompSg1 created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_dvcompsg1(
    dvcompsg1: DvCompSg1DTO, current_user: dict = Depends(auth_dependency)
):
    print(dvcompsg1)
    # print("Test successful: DvCompSg1 configuration is valid")
    # return response(200, "DvCompSg1 test successful")
    # return (400, "Gahalat sql likhi hai")
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in dvcompsg1.dict().items():
            if value is not None:
                print(f"{field}: {value}")
                
        filter_query = f"SELECT * FROM tst1a.datasets"
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

        # print("\n\nTest successful: DvCompSg1 configuration is valid\n\n")
        # return response(200, "DvCompSg1 test successful")

    except Exception as e:
        return response(400, str(e))

    
@router.post("/columns")
async def get_columns():
    try:
        filter_query = f"SELECT * FROM tst1a.datastores"
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
            200, "Test connection successful!", data=headers
        )
    except Exception as e:
        return response(400, str(e))
