from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvcompdl import (
    router,
    auth_dependency,
    get_db,
    response,
    RdvCompDlDTO,
)


@router.put("/update/{rdvid}")
async def update_rdvcompdl(
    rdvid: int, rdvcompdl: RdvCompDlDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT rdvid FROM tst1a.rdvcompdl WHERE rdvid = %s",
                (rdvid,),
            )
            if not cursor.fetchone():
                return response(404, "RdvCompDl not found")

            cursor.execute(
                """
                UPDATE tst1a.rdvcompdl SET 
                    projectshortname = %s,
                    dpname = %s,
                    dsname = %s,
                    comptype = %s,
                    compname = %s,
                    compkeyname = %s,
                    hubnums = %s,
                    hubnum = %s,
                    hubname = %s,
                    hubversion = %s,
                    bkfields = %s,
                    degen = %s,
                    degenids = %s,
                    tenantid = %s,
                    bkcarea = %s,
                    compshortname = %s,
                    version = %s
                WHERE rdvid = %s
                """,
                (
                    rdvcompdl.projectshortname,
                    rdvcompdl.dpname,
                    rdvcompdl.dsname,
                    rdvcompdl.comptype,
                    rdvcompdl.compname,
                    rdvcompdl.compkeyname,
                    rdvcompdl.hubnums,
                    rdvcompdl.hubnum,
                    rdvcompdl.hubname,
                    rdvcompdl.hubversion,
                    rdvcompdl.bkfields,
                    rdvcompdl.degen,
                    rdvcompdl.degenids,
                    rdvcompdl.tenantid,
                    rdvcompdl.bkcarea,
                    rdvcompdl.compshortname,
                    rdvcompdl.version,
                    rdvid,
                ),
            )
            conn.commit()

            return response(200, "RdvCompDl updated successfully")
    except Exception as e:
        return response(400, str(e))
