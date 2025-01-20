from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvbojds import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_rdvbojds(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    rdvid, projectshortname, dpname, dsname,
                    comptype, compname, satlnums, satlnum,
                    satlname, satlversion, tenantid, bkcarea,
                    createdate, compshortname, user_email,
                    comments, version
                FROM tst1a.rdvbojds 
                ORDER BY createdate DESC
                """
            )
            rdvbojds_list = []
            for rdv in cursor.fetchall():
                rdvbojds_dict = {
                    "rdvid": rdv[0],
                    "projectshortname": rdv[1],
                    "dpname": rdv[2],
                    "dsname": rdv[3],
                    "comptype": rdv[4],
                    "compname": rdv[5],
                    "satlnums": rdv[6],
                    "satlnum": rdv[7],
                    "satlname": rdv[8],
                    "satlversion": float(rdv[9]) if rdv[9] else None,
                    "tenantid": rdv[10],
                    "bkcarea": rdv[11],
                    "createdate": str(rdv[12]),
                    "compshortname": rdv[13],
                    "user_email": rdv[14],
                    "comments": rdv[15],
                    "version": float(rdv[16]) if rdv[16] else None,
                }
                rdvbojds_list.append(rdvbojds_dict)
        return response(200, "RdvBojDs fetched successfully", data=rdvbojds_list)
    except Exception as e:
        return response(400, str(e))
