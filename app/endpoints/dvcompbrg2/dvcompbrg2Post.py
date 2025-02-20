import pandas as pd
from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompbrg2 import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompBrgDTO,
)
from app.db import get_sqlalchemy_conn
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError

@router.post("/create")
async def create_dvcompbrg2(
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
                    version, processtype, datefieldname,user_email,hubnums,hubnum,hubname,
                    hubversion,bkfields,lnknums,lnknum,lnkname,
                    lnkversion,lnkbkfields
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
                    current_user["sub"],
                    dvcompbrg.hubnums,
                    dvcompbrg.hubnum,
                    dvcompbrg.hubname,
                    dvcompbrg.hubversion,
                    dvcompbrg.bkfields,
                    dvcompbrg.lnknums,
                    dvcompbrg.lnknum,
                    dvcompbrg.lnkname,
                    dvcompbrg.lnkversion,
                    dvcompbrg.lnkbkfields
                ),
            )
            conn.commit()

            return response(201, "DvCompBrg created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_dvcompbrg2(
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
                
                
        filter_query = dvcompbrg.sqltext;
        conn = get_sqlalchemy_conn()
        df = pd.read_sql(filter_query, conn)
        print(df)
        if df.empty:
            return response(404, "Dataset not found.")
        conn.commit()
        df = df.replace({float('nan'): None})
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
    
@router.post("/get-columns")
async def get_table_columns(data: dict, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        print("data:\n\n")
        for field, value in data.items():
            print(f"{field}: {value}")
            

        with get_db() as (conn, cursor):
            # Use pandas to get column information
            # query = f"SELECT * FROM tst1a.datasets"
            query = data['sqltext']
            print("query : ", query)
            df = pd.read_sql(query, conn)
            columns = df.columns.tolist()
            print("columns : ", columns)
            return response(200, "Columns fetched successfully", data=columns)
            
    except SQLAlchemyError as e:
        # Handle SQLAlchemy-related exceptions
        return response(400, f"Database error: {str(e)}")
    except Exception as e:
        return response(400, str(e))
