from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dataset import router, auth_dependency, get_db, response, Dataset


@router.put("/update/{datasetid}")
async def update_dataset(
    datasetid: int, dataset: Dataset, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if dataset exists
            cursor.execute(
                "SELECT datasetid FROM tst1a.datasets WHERE datasetid = %s",
                (datasetid,),
            )
            if not cursor.fetchone():
                return response(404, "Dataset not found")

            cursor.execute(
                """
                UPDATE tst1a.datasets SET 
                    projectshortname = %s,
                    dataproductshortname = %s,
                    datasetshortname = %s,
                    domainshortname = %s,
                    datastoreshortname = %s,
                    tablename = %s,
                    dsdatatype = %s,
                    fieldname = %s,
                    csvdailysuffix = %s,
                    csvname = %s,
                    separator = %s,
                    sourcename = %s,
                    tenantid = %s,
                    bkcarea = %s,
                    is_valid = %s
                WHERE datasetid = %s
                """,
                (
                    dataset.projectshortname,
                    dataset.dataproductshortname,
                    dataset.datasetshortname,
                    dataset.domainshortname,
                    dataset.datastoreshortname,
                    dataset.tablename,
                    dataset.dsdatatype,
                    dataset.fieldname,
                    dataset.csvdailysuffix,
                    dataset.csvname,
                    dataset.separator,
                    dataset.sourcename,
                    dataset.tenantid,
                    dataset.bkcarea,
                    True,
                    datasetid,
                ),
            )
            conn.commit()

            return response(200, "Dataset updated successfully")
    except Exception as e:
        return response(400, str(e))
