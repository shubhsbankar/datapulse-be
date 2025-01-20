from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvcompdh import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_rdvcompdh(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    rdvid, projectshortname, dpname, dsname,
                    comptype, compname, compkeyname, bkfields,
                    tenantid, bkcarea, createdate, compshortname,
                    user_email, version
                FROM tst1a.rdvcompdh 
                ORDER BY createdate DESC
                """
            )
            rdvcompdh_list = []
            for rdv in cursor.fetchall():
                rdvcompdh_dict = {
                    "rdvid": rdv[0],
                    "projectshortname": rdv[1],
                    "dpname": rdv[2],
                    "dsname": rdv[3],
                    "comptype": rdv[4],
                    "compname": rdv[5],
                    "compkeyname": rdv[6],
                    "bkfields": rdv[7],
                    "tenantid": rdv[8],
                    "bkcarea": rdv[9],
                    "createdate": str(rdv[10]),
                    "compshortname": rdv[11],
                    "user_email": rdv[12],
                    "version": float(rdv[13]) if rdv[13] else None,
                }
                rdvcompdh_list.append(rdvcompdh_dict)
        return response(200, "RdvCompDh fetched successfully", data=rdvcompdh_list)
    except Exception as e:
        return response(400, str(e))
