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
                    rdvid, 
                    comptype, compsubtype,  createdate,  version
                FROM tst1a.dvcompsg2
                ORDER BY createdate DESC
                """
            )
            dvcompsg2s = cursor.fetchall()
            dvcompsg2_list = []
            for dv in dvcompsg2s:
                dvcompsg2_dict = {
                    "rdvid": dv[0],
                    "comptype": dv[1],
                    "compsubtype": dv[2],
                    "createdate": str(dv[3]),
                    "version": float(dv[4]) if dv[4] else None,
                }
                dvcompsg2_list.append(dvcompsg2_dict)
        return response(200, "DvCompSg2s fetched successfully", data=dvcompsg2_list)
    except Exception as e:
        return response(400, str(e))
