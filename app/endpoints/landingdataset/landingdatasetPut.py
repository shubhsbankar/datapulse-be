from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.landingdataset import router, auth_dependency, get_db, response, LandingDataset


@router.put("/update/{datasetid}")
async def update_landingdataset(
    datasetid: int, dataset: LandingDataset, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if dataset exists
            cursor.execute(
                "SELECT dlid FROM tst1a.lndds1 WHERE dlid = %s",
                (datasetid,),
            )
            if not cursor.fetchone():
                return response(404, "Dataset not found")

            cursor.execute(
                """
                UPDATE tst1a.lndds1 SET 
                    projectshortname = %s,
                    srcdatasetshortname = %s,
                    srcdataproductshortname = %s,
                    lnddatasetshortname = %s,
                    lnddataproductshortname = %s,
                    useremailid = %s,
                    comments = %s,
                    lnddsshortname = %s
                WHERE dlid = %s
                """,
                (
                    dataset.projectshortname,
                    dataset.srcdatasetshortname,
                    dataset.srcdataproductshortname, 
                    dataset.lnddatasetshortname,
                    dataset.lnddataproductshortname,
                    current_user["sub"],
                    dataset.comments,
                    dataset.lnddsshortname,
                    datasetid,
                ),
            )
            conn.commit()

            return response(200, "Dataset updated successfully")
    except Exception as e:
        return response(400, str(e))
