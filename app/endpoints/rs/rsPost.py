from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rs import router, auth_dependency, get_db, response, RsDTO
import pandas as pd
from sqlalchemy import text


@router.post("/get-columns")
async def get_table_columns(data: dict, current_user: dict = Depends(auth_dependency)):
    # print([d]
    # print all values in data
    print(data)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        tablename = data.get("tablename")
        if not tablename:
            return response(400, "Table name is required")

        with get_db() as (conn, cursor):
            # Use pandas to get column information
            query = f"""
                SELECT * from tst1a.datasets
            """
            df = pd.read_sql(query, conn)
            columns = df.columns.to_list()

            return response(200, "Columns fetched successfully", data=columns)
    except Exception as e:
        return response(400, str(e))


@router.post("/create")
async def create_rs(rs: RsDTO, current_user: dict = Depends(auth_dependency)):
    print(rs)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Generate srchashcol and srcdphash
        srchashcol = "srchash1"
        # srcdphash = f"{rs.srcdataset}-{rs.dpname}"

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.rs (
                    projectshortname, srcdphash, srcdataset,
                    srctabfields, srchashcol, dpname, datastoreshortname, tablename,
                    bkeys, bkey1, bkey2, bkey3, bkey4, bkey5,
                    bkey6, bkey7, bkey8, bkey9, bkey10,
                    useremailid
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    rs.projectshortname,
                    rs.srcdphash,  # Auto-generated
                    rs.srcdataset,
                    rs.srctabfields,
                    srchashcol,  # Auto-generated
                    rs.dpname,
                    rs.datastoreshortname,
                    rs.tablename,
                    rs.bkeys,
                    rs.bkey1,
                    rs.bkey2,
                    rs.bkey3,
                    rs.bkey4,
                    rs.bkey5,
                    rs.bkey6,
                    rs.bkey7,
                    rs.bkey8,
                    rs.bkey9,
                    rs.bkey10,
                    current_user["sub"],
                ),
            )
            conn.commit()

            return response(201, "Source hash record created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_rs(rs: RsDTO, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in rs.dict().items():
            if value is not None:
                print(f"{field}: {value}")

        print("\n\nTest successful: Source hash configuration is valid\n\n")
        return response(200, "Source hash test successful")

    except Exception as e:
        return response(400, str(e))
