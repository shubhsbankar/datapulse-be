from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvcompft import (
    router,
    auth_dependency,
    get_db,
    response,
    RdvCompFtDTO,
)


@router.put("/update/{rdvid}")
async def update_rdvcompft(
    rdvid: int, rdvcompft: RdvCompFtDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT rdvid FROM tst1a.rdvcompft WHERE rdvid = %s",
                (rdvid,),
            )
            if not cursor.fetchone():
                return response(404, "rdvcompft not found")

            cursor.execute(
                """
                UPDATE tst1a.rdvcompft SET 
                    projectshortname = %s,
                    comptype = %s,
                    compname = %s,
                    compsubtype = %s,
                    compshortname = %s,
                    version = %s,
                    comments = %s,
                    sqltext = %s
                WHERE rdvid = %s
                """,
                (
                    rdvcompft.projectshortname,
                    rdvcompft.comptype,
                    rdvcompft.compname,
                    rdvcompft.compsubtype,
                    rdvcompft.compshortname,
                    rdvcompft.version,
                    rdvcompft.comments,
                    rdvcompft.sqltext,
                    rdvid,
                ),
            )
            conn.commit()

            return response(200, "rdvcompft updated successfully")
    except Exception as e:
        return response(400, str(e))
