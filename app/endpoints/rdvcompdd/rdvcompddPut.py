from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvcompdd import (
    router,
    auth_dependency,
    get_db,
    response,
    RdvCompDdDTO,
)


@router.put("/update/{rdvid}")
async def update_rdvcompdd(
    rdvid: int, rdvcompdd: RdvCompDdDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT rdvid FROM tst1a.rdvcompdd WHERE rdvid = %s",
                (rdvid,),
            )
            if not cursor.fetchone():
                return response(404, "RdvCompDd not found")

            cursor.execute(
                """
                UPDATE tst1a.rdvcompdd SET 
                    projectshortname = %s,
                    comptype = %s,
                    compname = %s,
                    compsubtype = %s,
                    bkfields = %s,
                    compshortname = %s,
                    version = %s,
                    comments = %s,
                    sqltext = %s
                WHERE rdvid = %s
                """,
                (
                    rdvcompdd.projectshortname,
                    rdvcompdd.comptype,
                    rdvcompdd.compname,
                    rdvcompdd.compsubtype,
                    rdvcompdd.bkfields,
                    rdvcompdd.compshortname,
                    rdvcompdd.version,
                    rdvcompdd.comments,
                    rdvcompdd.sqltext,
                    rdvid,
                ),
            )
            conn.commit()

            return response(200, "RdvCompDd updated successfully")
    except Exception as e:
        return response(400, str(e))
