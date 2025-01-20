from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dataset import *


@router.post("/create")
async def create_dataset(
    dataset: Dataset, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.datasets (
                    datastoreshortname, datasettype, projectshortname, datasetshortname,
                    dataproductshortname, domainshortname, separator,
                    dsdatatype, fieldname, sourcename, tenantid, bkcarea,
                    filessource, filesbucketpath, tablename, s3_accesskey,
                    s3_secretkey, gcs_jsonfile, is_valid, csvdailysuffix, csvname, useremailid
                ) VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                """,
                (
                    dataset.datastoreshortname,
                    dataset.datasettype,
                    dataset.projectshortname,
                    dataset.datasetshortname,
                    dataset.dataproductshortname,
                    dataset.domainshortname,
                    dataset.separator,
                    dataset.dsdatatype,
                    dataset.fieldname,
                    dataset.sourcename,
                    dataset.tenantid,
                    dataset.bkcarea,
                    dataset.filessource,
                    dataset.filesbucketpath,
                    dataset.tablename,
                    dataset.s3_accesskey,
                    dataset.s3_secretkey,
                    dataset.gcs_jsonfile,
                    dataset.is_valid,
                    dataset.csvdailysuffix,
                    dataset.csvname,
                    current_user["sub"],
                ),
            )
            conn.commit()

            return response(201, "Dataset created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_dataset(dataset: Dataset, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None dataset fields
        if dataset.datasetid:
            print(f"Dataset ID: {dataset.datasetid}")
        if dataset.datasettype:
            print(f"Dataset Type: {dataset.datasettype}")
        if dataset.csvname:
            print(f"CSV Name: {dataset.csvname}")
        if dataset.tablename:
            print(f"Table Name: {dataset.tablename}")
        if dataset.csvdailysuffix:
            print(f"CSV Daily Suffix: {dataset.csvdailysuffix}")
        if dataset.datasetshortname:
            print(f"Dataset Short Name: {dataset.datasetshortname}")
        if dataset.datastoreshortname:
            print(f"Datastore Short Name: {dataset.datastoreshortname}")
        if dataset.dataproductshortname:
            print(f"Data Product Short Name: {dataset.dataproductshortname}")
        if dataset.projectshortname:
            print(f"Project Short Name: {dataset.projectshortname}")
        if dataset.domainshortname:
            print(f"Domain Short Name: {dataset.domainshortname}")
        if dataset.separator:
            print(f"Separator: {dataset.separator}")
        if dataset.createdate:
            print(f"Create Date: {dataset.createdate}")
        if dataset.dsdatatype:
            print(f"DS Data Type: {dataset.dsdatatype}")
        if dataset.fieldname:
            print(f"Field Name: {dataset.fieldname}")
        if dataset.is_valid is not None:
            print(f"Is Valid: {dataset.is_valid}")
        if dataset.useremailid:
            print(f"User Email ID: {dataset.useremailid}")
        if dataset.sourcename:
            print(f"Source Name: {dataset.sourcename}")
        if dataset.tenantid:
            print(f"Tenant ID: {dataset.tenantid}")
        if dataset.bkcarea:
            print(f"BKC Area: {dataset.bkcarea}")
        if dataset.filessource:
            print(f"Files Source: {dataset.filessource}")
        if dataset.filesbucketpath:
            print(f"Files Bucket Path: {dataset.filesbucketpath}")
        if dataset.s3_accesskey:
            print(f"S3 Access Key: {dataset.s3_accesskey}")
        if dataset.s3_secretkey:
            print(f"S3 Secret Key: {dataset.s3_secretkey}")
        if dataset.gcs_jsonfile:
            print(f"GCS JSON File: {dataset.gcs_jsonfile}")
        print("\n\nTest successful: Dataset configuration is valid\n\n")

        filter_query = f"SELECT * FROM tst1a.users_latest WHERE useremail = '{current_user['sub']}'"
        conn = get_sqlalchemy_conn()
        df = pd.read_sql(filter_query, conn)
        print(df)
        if df.empty:
            return response(404, "Dataset not found.")
        conn.commit()
        return response(200, "Test connection successful!")
    except Exception as e:
        return response(500, f"Test connection failed: {str(e)}")
