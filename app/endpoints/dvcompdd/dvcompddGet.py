from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompdd import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_dvcompdd(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    dvid, projectshortname, comptype, compname, compsubtype, bkfields,
                    createdate, compshortname, comments, datefieldname, sqltext,
                    version
                FROM tst1a.dvcompdd1 
                ORDER BY createdate DESC
                """
            )
            rdvcompdd_list = []
            for rdv in cursor.fetchall():
                rdvcompdd_dict = {
                    "dvid": rdv[0],
                    "projectshortname": rdv[1],
                    "comptype": rdv[2],
                    "compname": rdv[3],
                    "compsubtype": rdv[4],
                    "bkfields": rdv[5],
                    "createdate": str(rdv[6]),
                    "compshortname": rdv[7],
                    "comments" : rdv[8], 
                    "datefieldname" : rdv[9], 
                    "sqltext" : rdv[10],
                    "version": float(rdv[11]) if rdv[11] else None,
                }
                rdvcompdd_list.append(rdvcompdd_dict)
        return response(200, "DvCompDd fetched successfully", data=rdvcompdd_list)
    except Exception as e:
        return response(400, str(e))
