from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvcompds import (
    router,
    auth_dependency,
    get_db,
    response,
    RdvCompDsDTO,
)


@router.put("/update/{rdvid}")
async def update_rdvcompds(
    rdvid: int, rdvcompds: RdvCompDsDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT rdvid FROM tst1a.rdvcompds WHERE rdvid = %s",
                (rdvid,),
            )
            if not cursor.fetchone():
                return response(404, "RdvCompDs not found")

            cursor.execute(
                """
                UPDATE tst1a.rdvcompds SET 
                    projectshortname = %s,
                    dpname = %s,
                    dsname = %s,
                    comptype = %s,
                    satlname = %s,
                    satlattr = %s,
                    assoccomptype = %s,
                    assoccompname = %s,
                    tenantid = %s,
                    bkcarea = %s,
                    compshortname = %s,
                    version = %s,
                    datefieldname = %s
                WHERE rdvid = %s
                """,
                (
                    rdvcompds.projectshortname,
                    rdvcompds.dpname,
                    rdvcompds.dsname,
                    rdvcompds.comptype,
                    rdvcompds.satlname,
                    rdvcompds.satlattr,
                    rdvcompds.assoccomptype,
                    rdvcompds.assoccompname,
                    rdvcompds.tenantid,
                    rdvcompds.bkcarea,
                    rdvcompds.compshortname,
                    rdvcompds.version,
                    rdvcompds.datefieldname,
                    rdvid,
                ),
            )
            conn.commit()

            return response(200, "RdvCompDs updated successfully")
    except Exception as e:
        return response(400, str(e))
