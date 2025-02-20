from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompft import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_dvcompft(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    dvid, projectshortname, comptype, compname, compsubtype, 
                    createdate, compshortname, comments, datefieldname, sqltext,
                    version, ddnums, ddnum, ddname, ddversion, bkfields
                FROM tst1a.dvcompft1 
                ORDER BY createdate DESC
                """
            )
            rdvcompft_list = []
            for rdv in cursor.fetchall():
                rdvcompft_dict = {
                    "dvid": rdv[0],
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
                    "ddnums": rdv[11],
                    "ddnum": rdv[12],
                    "ddname": rdv[13],
                    "ddversion": float(rdv[14]) if rdv[14] else None,
                    "bkfields": rdv[15]
                }
                rdvcompft_list.append(rdvcompft_dict)
        return response(200, "DvCompFT fetched successfully", data=rdvcompft_list)
    except Exception as e:
        return response(400, str(e))
