from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rt import *


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
async def create_rt(rt: RtDTO, current_user: dict = Depends(auth_dependency)):
    print(rt)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.rt (
                    projectshortname, tgtdphash, tgtdataset,
                    tgttabfields, tgthashcol, dpname, datastoreshortname, tablename,
                    bkeys, bkey1, bkey2, bkey3, bkey4, bkey5,
                    bkey6, bkey7, bkey8, bkey9, bkey10, useremailid
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    rt.projectshortname,
                    rt.tgtdphash,
                    rt.tgtdataset,
                    rt.tgttabfields,
                    rt.tgthashcol,
                    rt.dpname,
                    rt.datastoreshortname,
                    rt.tablename,
                    rt.bkeys,
                    rt.bkey1,
                    rt.bkey2,
                    rt.bkey3,
                    rt.bkey4,
                    rt.bkey5,
                    rt.bkey6,
                    rt.bkey7,
                    rt.bkey8,
                    rt.bkey9,
                    rt.bkey10,
                    current_user["sub"],
                ),
            )
            conn.commit()

            return response(201, "Target hash record created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_rt(rt: RtDTO, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in rt.dict().items():
            if value is not None:
                print(f"{field}: {value}")

        print("\n\nTest successful: Target hash configuration is valid\n\n")
        return response(200, "Target hash test successful")

    except Exception as e:
        return response(400, str(e))


@router.post("/get-tables")
async def get_table_names(data: dict, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        projectshortname = data.get("projectshortname")
        if not projectshortname:
            return response(400, "Project short name is required")

        datasetname = data.get("datasetname")
        if not datasetname:
            return response(400, "Dataset name is required")
        
        datastoreshortname = data.get("datastoreshortname")
        if not datastoreshortname:
            return response(400, "Datastore short name is required")
        
        dataproductshortname = data.get("dataproductshortname")
        if not dataproductshortname:
            return response(400, "Dataproduct short name is required")
        for k, v in data.items():
            print(f"{k}: {v}")

        with get_db() as (conn, cursor):
            # Use pandas to get tables for the dataset
            query = f"""SELECT tablename FROM tst1a.datasets where
            projectshortname = '{projectshortname}' and
            datasetshortname = '{datasetname}' and datastoreshortname = '{datastoreshortname}' and dataproductshortname = '{dataproductshortname}'"""
            # query = f"SELECT * FROM tst1a."
            df = pd.read_sql(query, conn)
            print(df)
            tables = df["tablename"].tolist()
            print(tables)
            # tables = ["table1", "table2", "table3"]

            return response(200, "Tables fetched successfully", data=tables)
    except Exception as e:
        return response(400, str(e))
