from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompft import *
from sqlalchemy.exc import SQLAlchemyError

@router.post("/create")
async def create_dvcompft(
    rdvcompft: DvCompFtDTO, current_user: dict = Depends(auth_dependency)
):
    print(rdvcompft)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        # >> compshortname is not getting inserted, its the concat of projectshortname, dpname, dsname, compname, version
        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.dvcompft1 (
                    projectshortname, comptype,
                    compname, compsubtype, compshortname, version,
                    comments, sqltext, datefieldname,user_email,
                    ddnums, ddnum, ddname, ddversion, bkfields
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    rdvcompft.projectshortname,
                    rdvcompft.comptype,
                    rdvcompft.compname,
                    rdvcompft.compsubtype,
                    rdvcompft.compshortname,
                    rdvcompft.version,
                    rdvcompft.comments,
                    rdvcompft.sqltext,
                    rdvcompft.datefieldname,
                    current_user["sub"],
                    rdvcompft.ddnums,
                    rdvcompft.ddnum,
                    rdvcompft.ddname,
                    rdvcompft.ddversion,
                    rdvcompft.bkfields
                ),
            )
            conn.commit()

            return response(201, "dvcompft created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_dvcompft(
    rdvcompft: DvCompFtDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        print("rdvcompft : ", rdvcompft)
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in rdvcompft.dict().items():
            if value is not None:
                print(f"{field}: {value}")

        filter_query = rdvcompft.sqltext
        conn = get_sqlalchemy_conn()
        df = pd.read_sql(filter_query, conn)
        print(df)
        if df.empty:
            return response(404, "Dataset not found.")
        conn.commit()
        # Replace NaN values with None before encoding
        df = df.replace({float('nan'): None})
        print("df : ", df)
        
        headers = jsonable_encoder(df.columns.tolist())
        rows = jsonable_encoder(df.values.tolist())
        if df.empty:
            return response(404, "Dataset not found.")
        conn.commit()
        return response(
            200, "Test connection successful!", data={"headers": headers, "rows": rows}
        )
        # print("\n\nTest successful: RdvCompDh configuration is valid\n\n")
        # return response(200, "RdvCompDh test successful")

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
