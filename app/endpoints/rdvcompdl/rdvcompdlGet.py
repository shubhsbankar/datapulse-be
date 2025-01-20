from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvcompdl import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_rdvcompdl(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    rdvid, projectshortname, dpname, dsname,
                    comptype, compname, compkeyname, hubnums,
                    hubnum, hubname, hubversion, bkfields,
                    degen, degenids, tenantid, bkcarea,
                    createdate, user_email, compshortname, version
                FROM tst1a.rdvcompdl 
                ORDER BY createdate DESC
                """
            )
            rdvcompdl_list = []
            for rdv in cursor.fetchall():
                rdvcompdl_dict = {
                    "rdvid": rdv[0],
                    "projectshortname": rdv[1],
                    "dpname": rdv[2],
                    "dsname": rdv[3],
                    "comptype": rdv[4],
                    "compname": rdv[5],
                    "compkeyname": rdv[6],
                    "hubnums": rdv[7],
                    "hubnum": rdv[8],
                    "hubname": rdv[9],
                    "hubversion": float(rdv[10]) if rdv[10] else None,
                    "bkfields": rdv[11],
                    "degen": rdv[12],
                    "degenids": rdv[13],
                    "tenantid": rdv[14],
                    "bkcarea": rdv[15],
                    "createdate": str(rdv[16]),
                    "user_email": rdv[17],
                    "compshortname": rdv[18],
                    "version": float(rdv[19]) if rdv[19] else None,
                }
                rdvcompdl_list.append(rdvcompdl_dict)
        return response(200, "RdvCompDl fetched successfully", data=rdvcompdl_list)
    except Exception as e:
        return response(400, str(e))
