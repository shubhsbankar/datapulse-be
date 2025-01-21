import pandas as pd
from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompbrg import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompBrgDTO,
)
from app.db import get_sqlalchemy_conn
from fastapi.encoders import jsonable_encoder


@router.post("/create")
async def create_dvcompbrg(
    dvcompbrg: DvCompBrgDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.dvcompbrg1 (
                    projectshortname, comptype,
                    compname, compsubtype, sqltext,  compshortname,  comments,
                    version, processtype, datefieldname,user_email
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s
                )
                """,
                (
                    dvcompbrg.projectshortname,
                    dvcompbrg.comptype,
                    dvcompbrg.compname,
                    dvcompbrg.compsubtype,
                    dvcompbrg.sqltext,
                    dvcompbrg.compshortname,
                    dvcompbrg.comments,
                    dvcompbrg.version,
                    dvcompbrg.processtype,
                    dvcompbrg.datefieldname,
                    current_user["sub"]
                ),
            )
            conn.commit()

            return response(201, "DvCompBrg created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_dvcompbrg(
    dvcompbrg: DvCompBrgDTO, current_user: dict = Depends(auth_dependency)
):
    print(dvcompbrg)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in dvcompbrg.dict().items():
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
async def get_dvcompbrg_columns():
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
