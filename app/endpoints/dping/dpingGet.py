from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dping import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_dpings(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    dpid, dpshortname, htmlfilename, datasettype,
                    projectshortname, datasetshortname, dataproductshortname,
                    createdate, useremailid
                FROM tst1a.dping 
                ORDER BY createdate DESC
                """
            )
            dpings = cursor.fetchall()
            dping_list = []
            for dp in dpings:
                dping_dict = {
                    "dpid": dp[0],
                    "dpshortname": dp[1],
                    "htmlfilename": dp[2],
                    "datasettype": dp[3],
                    "projectshortname": dp[4],
                    "datasetshortname": dp[5],
                    "dataproductshortname": dp[6],
                    "createdate": str(dp[7]),
                    "useremailid": dp[8],
                }
                dping_list.append(dping_dict)
        return response(200, "Dpings fetched successfully", data=dping_list)
    except Exception as e:
        return response(400, str(e))
