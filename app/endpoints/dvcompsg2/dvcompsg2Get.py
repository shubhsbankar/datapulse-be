from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompsg2 import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_dvcompsg2s(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    dvid, projectshortname, 
                    comptype, compname, compsubtype, sqltext,
                    createdate, compshortname,
                    user_email, comments, version
                FROM tst1a.dvcompddl1 
                ORDER BY createdate DESC
                """
            )
            dvcompsg2s = cursor.fetchall()
            dvcompsg2_list = []
            for dv in dvcompsg2s:
                dvcompsg2_dict = {
                    "dvid": dv[0],
                    "projectshortname": dv[1],
                    "comptype": dv[2],
                    "compname": dv[3],
                    "compsubtype": dv[4],
                    "sqltext": dv[5],
                    "createdate": str(dv[6]),
                    "compshortname": dv[7],
                    "user_email": dv[8],
                    "comments": dv[9],
                    "version": float(dv[10]) if dv[10] else None
                }
                dvcompsg2_list.append(dvcompsg2_dict)
        return response(200, "DvCompSg2s fetched successfully", data=dvcompsg2_list)
    except Exception as e:
        return response(400, str(e))
