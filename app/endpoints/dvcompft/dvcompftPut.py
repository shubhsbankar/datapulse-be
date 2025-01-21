from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompft import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompFtDTO,
)


@router.put("/update/{dvid}")
async def update_dvcompft(
    dvid: int, rdvcompft: DvCompFtDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT dvid FROM tst1a.dvcompft1 WHERE dvid = %s",
                (dvid,),
            )
            if not cursor.fetchone():
                return response(404, "dvcompft not found")

            cursor.execute(
                """
                UPDATE tst1a.dvcompft1 SET 
                    projectshortname = %s,
                    comptype = %s,
                    compname = %s,
                    compsubtype = %s,
                    compshortname = %s,
                    version = %s,
                    comments = %s,
                    sqltext = %s
                WHERE dvid = %s
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
                    dvid,
                ),
            )
            conn.commit()

            return response(200, "dvcompft updated successfully")
    except Exception as e:
        return response(400, str(e))
