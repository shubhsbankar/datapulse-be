from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompsg1 import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_dvcompsg1s(current_user: dict = Depends(auth_dependency)):
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
                    datefieldname,
                    partsnum, parts
                FROM tst1a.dvcompsg1 
                ORDER BY createdate DESC
                """
            )
            dvcompsg1s = cursor.fetchall()
            dvcompsg1_list = []
            for dv in dvcompsg1s:
                dvcompsg1_dict = {
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
                    "partsnum": dv[17],
                    "parts": dv[18],
                }
                dvcompsg1_list.append(dvcompsg1_dict)
        return response(200, "DvCompSg1s fetched successfully", data=dvcompsg1_list)
    except Exception as e:
        return response(400, str(e))
