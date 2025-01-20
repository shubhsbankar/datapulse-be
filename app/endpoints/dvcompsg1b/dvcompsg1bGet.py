from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompsg1b import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_dvcompsg1bs(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    rdvid, projectshortname,
                    comptype, compname, compsubtype, sqltext,
                    createdate, compshortname,
                    user_email, comments
                FROM tst1a.dvcompsg1b 
                ORDER BY createdate DESC
                """
            )
            dvcompsg1bs = cursor.fetchall()
            dvcompsg1b_list = []
            for dv in dvcompsg1bs:
                dvcompsg1b_dict = {
                    "rdvid": dv[0],
                    "projectshortname": dv[1],
                    "comptype": dv[2],
                    "compname": dv[3],
                    "compsubtype": dv[4],
                    "sqltext": dv[5],
                    "createdate": str(dv[6]),
                    "compshortname": dv[7],
                    "user_email": dv[8],
                    "comments": dv[9],
                }
                dvcompsg1b_list.append(dvcompsg1b_dict)
        return response(200, "DvCompSg1s fetched successfully", data=dvcompsg1b_list)
    except Exception as e:
        return response(400, str(e))
