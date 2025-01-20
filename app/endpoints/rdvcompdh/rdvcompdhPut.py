from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvcompdh import (
    router,
    auth_dependency,
    get_db,
    response,
    RdvCompDhDTO,
)


@router.put("/update/{rdvid}")
async def update_rdvcompdh(
    rdvid: int, rdvcompdh: RdvCompDhDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT rdvid FROM tst1a.rdvcompdh WHERE rdvid = %s",
                (rdvid,),
            )
            if not cursor.fetchone():
                return response(404, "RdvCompDh not found")

            cursor.execute(
                """
                UPDATE tst1a.rdvcompdh SET 
                    projectshortname = %s,
                    dpname = %s,
                    dsname = %s,
                    comptype = %s,
                    compname = %s,
                    compkeyname = %s,
                    bkfields = %s,
                    tenantid = %s,
                    bkcarea = %s,
                    compshortname = %s,
                    version = %s
                WHERE rdvid = %s
                """,
                (
                    rdvcompdh.projectshortname,
                    rdvcompdh.dpname,
                    rdvcompdh.dsname,
                    rdvcompdh.comptype,
                    rdvcompdh.compname,
                    rdvcompdh.compkeyname,
                    rdvcompdh.bkfields,
                    rdvcompdh.tenantid,
                    rdvcompdh.bkcarea,
                    rdvcompdh.compshortname,
                    rdvcompdh.version,
                    rdvid,
                ),
            )
            conn.commit()

            return response(200, "RdvCompDh updated successfully")
    except Exception as e:
        return response(400, str(e))
