from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dataset import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_datasets(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    datastoreshortname, datasettype, projectshortname, datasetshortname,
                    dataproductshortname, domainshortname, separator,
                    dsdatatype, fieldname, sourcename, tenantid, bkcarea,
                    filessource, filesbucketpath, tablename, s3_accesskey,
                    s3_secretkey, gcs_jsonfile, is_valid, csvdailysuffix, csvname, separator, useremailid, createdate, datasetid
                FROM tst1a.datasets 
                ORDER BY createdate DESC
                """
            )
            datasets = cursor.fetchall()
            dataset_list = []
            for ds in datasets:
                dataset_dict = {
                    "datastoreshortname": ds[0],
                    "datasettype": ds[1],
                    "projectshortname": ds[2],
                    "datasetshortname": ds[3],
                    "dataproductshortname": ds[4],
                    "domainshortname": ds[5],
                    "separator": ds[6],
                    "dsdatatype": ds[7],
                    "fieldname": ds[8],
                    "sourcename": ds[9],
                    "tenantid": ds[10],
                    "bkcarea": ds[11],
                    "filessource": ds[12],
                    "filesbucketpath": ds[13],
                    "tablename": ds[14],
                    "s3_accesskey": ds[15],
                    "s3_secretkey": ds[16],
                    "gcs_jsonfile": ds[17],
                    "is_valid": ds[18],
                    "csvdailysuffix": ds[19],
                    "csvname": ds[20],
                    "separator": ds[21],
                    "useremailid": ds[22],
                    "createdate": str(ds[23]),
                    "datasetid": ds[24],
                }
                dataset_list.append(dataset_dict)
        return response(200, "Datasets fetched successfully", data=dataset_list)
    except Exception as e:
        return response(400, str(e))


@router.get("/{dsid}")
async def get_dataset_by_id(dsid: int, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT datasetid, projectshortname, dataproductshortname, datasetshortname, domainshortname, datastoreshortname, tablename, dsdatatype, fieldname, sourcename, tenantid, bkcarea, is_valid, createdate, useremailid 
                FROM tst1a.datasets 
                WHERE datasetid = %s
                """,
                (dsid,),
            )
            dataset = cursor.fetchone()
            if not dataset:
                return response(404, "Dataset not found")

            dataset_dict = {
                "datasetid": dataset[0],
                "projectshortname": dataset[1],
                "dataproductshortname": dataset[2],
                "datasetshortname": dataset[3],
                "domainshortname": dataset[4],
                "datastoreshortname": dataset[5],
                "tablename": dataset[6],
                "dsdatatype": dataset[7],
                "fieldname": dataset[8],
                "sourcename": dataset[9],
                "tenantid": dataset[10],
                "bkcarea": dataset[11],
                "is_valid": dataset[12],
                "createdate": str(dataset[13]),
                "useremail": dataset[14],
            }
            return response(200, "Dataset fetched successfully", data=dataset_dict)
    except Exception as e:
        return response(400, str(e))
