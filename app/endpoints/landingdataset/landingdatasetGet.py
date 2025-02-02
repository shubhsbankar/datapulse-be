from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.landingdataset import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_landingdatasets(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            try:
                cursor.execute(
                    """
                    SELECT 
                        projectshortname, srcdatasetshortname,
                        srcdataproductshortname, lnddataproductshortname, lnddatasetshortname,                    
                        useremailid, createdate, dlid, comments, lnddsshortname
                    FROM tst1a.lndds1 
                    ORDER BY createdate DESC
                    """
                )
                datasets = cursor.fetchall()
                dataset_list = []
                for ds in datasets:
                    # Add null checks for each field
                    dataset_dict = {
                        "projectshortname": ds[0] if ds[0] is not None else "",
                        "srcdatasetshortname": ds[1] if ds[1] is not None else "",
                        "srcdataproductshortname": ds[2] if ds[2] is not None else "",
                        "lnddataproductshortname": ds[3] if ds[3] is not None else "",
                        "lnddatasetshortname": ds[4] if ds[4] is not None else "",
                        "useremailid": ds[5] if ds[5] is not None else "",
                        "createdate": ds[6].isoformat() if ds[6] is not None else "",
                        "dlid": ds[7] if ds[7] is not None else "",
                        "comments": ds[8] if ds[8] is not None else "",
                        "lnddsshortname": ds[9] if ds[9] is not None else ""
                    }
                    dataset_list.append(dataset_dict)
                return response(200, "Landing Datasets fetched successfully", data=dataset_list)
            except Exception as db_error:
                print(f"Database error: {str(db_error)}")
                return response(400, f"Database error: {str(db_error)}")
    except Exception as e:
        print(f"General error: {str(e)}")
        return response(400, str(e))


@router.get("/{dlid}")
async def get_landingdataset_by_id(dlid: int, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT projectshortname, srcdatasetshortname,
                    srcdataproductshortname, lnddatasetshortname, lnddatasetshortname                    
                    useremailid, createdate, dlid, comments, lnddsshortname 
                WHERE dlid = %s
                """,
                (dlid,),
            )
            ds = cursor.fetchone()
            if not ds:
                return response(404, "Dataset not found")

            dataset_dict = {
                    "projectshortname": ds[0],
                    "srcdatasetshortname": ds[1],
                    "srcdataproductshortname": ds[2],
                    "lnddatasetshortname": ds[3],
                    "lnddatasetshortname": ds[4],
                    "useremailid": ds[5],
                    "createdate": ds[6],
                    "dlid": ds[7],
                    "comments": ds[8],
                    "lnddsshortname": ds[9]
            }
            return response(200, "Landing Dataset fetched successfully", data=dataset_dict)
    except Exception as e:
        return response(400, str(e))
