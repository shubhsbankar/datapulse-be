from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvbojsg1 import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_dvbojsg1s(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    rdvid, projectshortname, dpname, dsname,
                    comptype, compname, compsubtype, sqltext,
                    tenantid, bkcarea, createdate, compshortname,
                    user_email, comments, version, processtype,
                    datefieldname, parts, partsnum
                FROM tst1a.dvbojsg1 
                ORDER BY createdate DESC
                """
            )
            dvbojsg1s = cursor.fetchall()
            dvbojsg1_list = []
            for dv in dvbojsg1s:
                dvbojsg1_dict = {
                    "rdvid": dv[0],
                    "projectshortname": dv[1],
                    "dpname": dv[2],
                    "dsname": dv[3],
                    "comptype": dv[4],
                    "compname": dv[5],
                    "compsubtype": dv[6],
                    "sqltext": dv[7],
                    "tenantid": dv[8],
                    "bkcarea": dv[9],
                    "createdate": str(dv[10]),
                    "compshortname": dv[11],
                    "user_email": dv[12],
                    "comments": dv[13],
                    "version": float(dv[14]) if dv[14] else None,
                    "processtype": dv[15],
                    "datefieldname": dv[16],
                    "parts": dv[17],
                    "partsnum": dv[18],
                }
                dvbojsg1_list.append(dvbojsg1_dict)
        return response(200, "DvBojSg1s fetched successfully", data=dvbojsg1_list)
    except Exception as e:
        return response(400, str(e))
