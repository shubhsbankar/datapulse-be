from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvbojds import (
    router,
    auth_dependency,
    get_db,
    response,
    RdvBojDsDTO,
)


@router.put("/update/{rdvid}")
async def update_rdvbojds(
    rdvid: int, rdvbojds: RdvBojDsDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT rdvid FROM tst1a.rdvbojds WHERE rdvid = %s",
                (rdvid,),
            )
            if not cursor.fetchone():
                return response(404, "RdvBojDs not found")

            cursor.execute(
                """
                UPDATE tst1a.rdvbojds SET 
                    projectshortname = %s,
                    dpname = %s,
                    dsname = %s,
                    comptype = %s,
                    compname = %s,
                    satlnums = %s,
                    satlnum = %s,
                    satlname = %s,
                    satlversion = %s,
                    tenantid = %s,
                    bkcarea = %s,
                    compshortname = %s,
                    comments = %s,
                    version = %s
                WHERE rdvid = %s
                """,
                (
                    rdvbojds.projectshortname,
                    rdvbojds.dpname,
                    rdvbojds.dsname,
                    rdvbojds.comptype,
                    rdvbojds.compname,
                    rdvbojds.satlnums,
                    rdvbojds.satlnum,
                    rdvbojds.satlname,
                    rdvbojds.satlversion,
                    rdvbojds.tenantid,
                    rdvbojds.bkcarea,
                    rdvbojds.compshortname,
                    rdvbojds.comments,
                    rdvbojds.version,
                    rdvid,
                ),
            )
            conn.commit()

            return response(200, "RdvBojDs updated successfully")
    except Exception as e:
        return response(400, str(e))
