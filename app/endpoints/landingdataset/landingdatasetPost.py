from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.landingdataset import *


@router.post("/create")
async def create_landingdataset(
    dataset: LandingDataset, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        print(dataset)
        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.lndds1 (
                    projectshortname, srcdatasetshortname,
                    srcdataproductshortname, lnddataproductshortname, lnddatasetshortname,                   
                    useremailid, comments, lnddsshortname
                ) VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s
                )
                """,
                (
                    dataset.projectshortname,
                    dataset.srcdatasetshortname,
                    dataset.srcdataproductshortname,
                    dataset.lnddataproductshortname,
                    dataset.lnddatasetshortname,
                    current_user["sub"],
                    dataset.comments,
                    dataset.lnddsshortname
                ),
            )
            conn.commit()

            return response(201, "Dataset created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_landingdataset(dataset: LandingDataset, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None dataset fields
        if dataset.dlid:
            print(f"Dataset ID: {dataset.dlid}")
        if dataset.projectshortname:
            print(f"Project Short Name: {dataset.projectshortname}")
        if dataset.srcdatasetshortname:
            print(f"Source Dataset Short Name: {dataset.srcdatasetshortname}")
        if dataset.srcdataproductshortname:
            print(f"Source Data Product Short Name: {dataset.srcdataproductshortname}")
        if dataset.lnddatasetshortname:
            print(f"Landing Dataset Short Name: {dataset.lnddatasetshortname}")
        if dataset.lnddataproductshortname:
            print(f"Landing Dataset Product Short Name: {dataset.lnddataproductshortname}")
        if dataset.lnddsshortname:
            print(f"Landing Dataset Short Name: {dataset.lnddsshortname}")
        if dataset.createdate:
            print(f"Create Date: {dataset.createdate}")
        if dataset.useremailid:
            print(f"User Email ID: {dataset.useremailid}")
        if dataset.comments:
            print(f"Comments: {dataset.comments}")
        print("\n\nTest successful: Dataset configuration is valid\n\n")

        filter_query = f"SELECT * FROM tst1a.lndds1"
        conn = get_sqlalchemy_conn()
        df = pd.read_sql(filter_query, conn)
        print(df)
        # if df.empty:
        #     return response(404, "Dataset not found.")
        conn.commit()
        return response(200, "Test connection successful!")
    except Exception as e:
        return response(500, f"Test connection failed: {str(e)}")
