from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvcompft import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_rdvcompft(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    rdvid, projectshortname, comptype, compname, compsubtype, 
                    createdate, compshortname, comments, datefieldname, sqltext,
                    version
                FROM tst1a.rdvcompft 
                ORDER BY createdate DESC
                """
            )
            rdvcompft_list = []
            for rdv in cursor.fetchall():
                rdvcompft_dict = {
                    "rdvid": rdv[0],
                    "projectshortname": rdv[1],
                    "comptype": rdv[2],
                    "compname": rdv[3],
                    "compsubtype": rdv[4],
                    "createdate": str(rdv[5]),
                    "compshortname": rdv[6],
                    "comments" : rdv[7], 
                    "datefieldname" : rdv[8], 
                    "sqltext" : rdv[9],
                    "version": float(rdv[10]) if rdv[10] else None,
                }
                rdvcompft_list.append(rdvcompft_dict)
        return response(200, "RdvCompDd fetched successfully", data=rdvcompft_list)
    except Exception as e:
        return response(400, str(e))
