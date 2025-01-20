from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.endpoints.dtg import *


@router.post("/create")
async def create_dtg(dtg: DtgDTO, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.dtg (
                    dtshortname, chkfilename, datasettype,
                    datasrcnum, projectshortname, datasetshortname,
                    dataproductshortname, useremailid,
                    testcoverageversion, comments
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    dtg.dtshortname,
                    dtg.chkfilename,
                    dtg.datasettype,
                    dtg.datasrcnum,
                    dtg.projectshortname,
                    dtg.datasetshortname,
                    dtg.dataproductshortname,
                    current_user["sub"],
                    dtg.testcoverageversion,
                    dtg.comments,
                ),
            )
            conn.commit()

            return response(201, "DTG created successfully")
    except Exception as e:
        if str(e).strip().startswith("duplicate key value"):
            return response(400, "DTG already exists.")
        return response(400, str(e))


@router.post("/sql/execute")
async def test_dtg(dtg: SqlExecuteDTO, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None dtg fields for testing
        if dtg.projectshortname:
            print(f"Project Short Name: {dtg.projectshortname}")
        if dtg.datasetshortname:
            print(f"Dataset Short Name: {dtg.datasetshortname}")
        if dtg.dataproductshortname:
            print(f"Data Product Short Name: {dtg.dataproductshortname}")
        if dtg.testcoverageversion:
            print(f"Test Coverage Version: {dtg.testcoverageversion}")
        if dtg.sqlQuery:
            print(f"Dataset Short Name: {dtg.datasetshortname}")
        if dtg.dataproductshortname:
            print(f"Data Product Short Name: {dtg.dataproductshortname}")
        if dtg.testcoverageversion:
            print(f"Test Coverage Version: {dtg.testcoverageversion}")
        if dtg.executiondate:
            print(f"Execution Date: {dtg.executiondate}")

        filter_query = dtg.sqlQuery
        # filter_query = f"SELECT * FROM tst1a.dtg"
        conn = get_sqlalchemy_conn()
        try:
            df = pd.read_sql(filter_query, conn)
        except Exception as e:
            return response(400, f"Test connection failed: {str(e)}")
        # print(dtg.sqlQuery)
        print(df)
        headers = jsonable_encoder(df.columns.tolist())
        rows = jsonable_encoder(df.values.tolist())
        if df.empty:
            return response(404, "Dataset not found.")
        conn.commit()
        return response(
            200, "Test connection successful!", data={"headers": headers, "rows": rows}
        )
    except Exception as e:
        return response(500, f"Test connection failed: {str(e)}")
