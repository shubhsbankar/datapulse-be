from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dtg import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_dtgs(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    dtid, dtshortname, chkfilename, datasettype,
                    datasrcnum, projectshortname, datasetshortname,
                    dataproductshortname, createdate, useremailid,
                    testcoverageversion, comments
                FROM tst1a.dtg 
                ORDER BY createdate DESC
                """
            )
            dtgs = cursor.fetchall()
            dtg_list = []
            for dtg in dtgs:
                dtg_dict = {
                    "dtid": dtg[0],
                    "dtshortname": dtg[1],
                    "chkfilename": dtg[2],
                    "datasettype": dtg[3],
                    "datasrcnum": dtg[4],
                    "projectshortname": dtg[5],
                    "datasetshortname": dtg[6],
                    "dataproductshortname": dtg[7],
                    "createdate": str(dtg[8]),
                    "useremailid": dtg[9],
                    "testcoverageversion": dtg[10],
                    "comments": dtg[11],
                }
                dtg_list.append(dtg_dict)
        return response(200, "DTGs fetched successfully", data=dtg_list)
    except Exception as e:
        return response(400, str(e))
