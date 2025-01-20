from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompbrg import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompBrgDTO,
)


@router.put("/update/{dvid}")
async def update_dvcompbrg(
    dvid: int, dvcompbrg: DvCompBrgDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT rdvid FROM tst1a.dvcompbrg WHERE dvid = %s",
                (dvid,),
            )
            if not cursor.fetchone():
                return response(404, "DvCompBrg not found")

            cursor.execute(
                """
                UPDATE tst1a.dvcompbrg SET 
                    projectshortname = %s,
                    comptype = %s,
                    compname = %s,
                    compsubtype = %s,
                    sqltext = %s,
                    compshortname = %s,
                    comments = %s,
                    version = %s,
                    processtype = %s,
                    datefieldname = %s
                WHERE dvid = %s
                """,
                (
                    dvcompbrg.projectshortname,
                    dvcompbrg.comptype,
                    dvcompbrg.compname,
                    dvcompbrg.compsubtype,
                    dvcompbrg.sqltext,
                    dvcompbrg.compshortname,
                    dvcompbrg.comments,
                    dvcompbrg.version,
                    dvcompbrg.processtype,
                    dvcompbrg.datefieldname,
                    dvid,
                ),
            )
            conn.commit()

            return response(200, "DvCompBrg updated successfully")
    except Exception as e:
        return response(400, str(e))
