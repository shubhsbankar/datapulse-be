from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompsg2 import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompSg2DTO,
)
from fastapi.encoders import jsonable_encoder
from app.db import get_sqlalchemy_conn
import pandas as pd


@router.post("/create")
async def create_dvcompsg2(
    dvcompsg2: DvCompSg2DTO, current_user: dict = Depends(auth_dependency)
):
    print(dvcompsg2)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
               """
                INSERT INTO tst1a.dvcompddl1 (
                    projectshortname, comptype,
                    compname, compsubtype, sqltext, 
                    compshortname, user_email, comments,
                    version
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    dvcompsg2.projectshortname,
                    dvcompsg2.comptype,
                    dvcompsg2.compname,
                    dvcompsg2.compsubtype,
                    dvcompsg2.sqltext,
                    dvcompsg2.compshortname,
                    current_user["sub"],
                    dvcompsg2.comments,
                    dvcompsg2.version,
                ),
            )
            conn.commit()

            return response(201, "DvCompSg2 created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_dvcompsg2(
    dvcompsg2: DvCompSg2DTO, current_user: dict = Depends(auth_dependency)
):
    print(dvcompsg2)
    # print("Test successful: DvCompSg1 configuration is valid")
    # return response(200, "DvCompSg1 test successful")
    # return (400, "Gahalat sql likhi hai")
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in dvcompsg2.dict().items():
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
