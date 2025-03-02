from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvcompds import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_rdvcompds(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    rdvid, projectshortname, dpname, dsname,
                    comptype, satlname, satlattr, assoccomptype,
                    assoccompname, tenantid, bkcarea, createdate,
                    user_email, compshortname, version, partsnum, parts,
                    datefieldname
                FROM tst1a.rdvcompds 
                ORDER BY createdate DESC
                """
            )
            rdvcompds_list = []
            for rdv in cursor.fetchall():
                rdvcompds_dict = {
                    "rdvid": rdv[0],
                    "projectshortname": rdv[1],
                    "dpname": rdv[2],
                    "dsname": rdv[3],
                    "comptype": rdv[4],
                    "satlname": rdv[5],
                    "satlattr": rdv[6],
                    "assoccomptype": rdv[7],
                    "assoccompname": rdv[8],
                    "tenantid": rdv[9],
                    "bkcarea": rdv[10],
                    "createdate": str(rdv[11]),
                    "user_email": rdv[12],
                    "compshortname": rdv[13],
                    "version": float(rdv[14]) if rdv[14] else None,
                    "partsnum": rdv[15],
                    "parts": rdv[16],
                    "datefieldname": rdv[17]
                }
                rdvcompds_list.append(rdvcompds_dict)
        return response(200, "RdvCompDs fetched successfully", data=rdvcompds_list)
    except Exception as e:
        return response(400, str(e))
