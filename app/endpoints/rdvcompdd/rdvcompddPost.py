from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvcompdd import *


@router.post("/create")
async def create_rdvcompdd(
    rdvcompdd: RdvCompDdDTO, current_user: dict = Depends(auth_dependency)
):
    print(rdvcompdd)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        # >> compshortname is not getting inserted, its the concat of projectshortname, dpname, dsname, compname, version
        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.rdvcompdd (
                    projectshortname, comptype,
                    compname, compsubtype, bkfields, compshortname, version,
                    comments, sqltext, datefieldname
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s,%s
                )
                """,
                (
                    rdvcompdd.projectshortname,
                    rdvcompdd.comptype,
                    rdvcompdd.compname,
                    rdvcompdd.compsubtype,
                    rdvcompdd.bkfields,
                    rdvcompdd.compshortname,
                    rdvcompdd.version,
                    rdvcompdd.comments,
                    rdvcompdd.sqltext,
                    rdvcompdd.datefieldname
                ),
            )
            conn.commit()

            return response(201, "RdvCompDd created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_rdvcompdd(
    rdvcompdd: RdvCompDdDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in rdvcompdd.dict().items():
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
            query = f"SELECT * FROM tst1a.datasets"
            df = pd.read_sql(query, conn)
            columns = df.columns.tolist()

            return response(200, "Columns fetched successfully", data=columns)
    except Exception as e:
        return response(400, str(e))
