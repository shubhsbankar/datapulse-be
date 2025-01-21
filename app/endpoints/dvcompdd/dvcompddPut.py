from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompdd import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompDdDTO,
)


@router.put("/update/{dvid}")
async def update_dvcompdd(
    dvid: int, rdvcompdd: DvCompDdDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT dvid FROM tst1a.dvcompdd1 WHERE dvid = %s",
                (dvid,),
            )
            if not cursor.fetchone():
                return response(404, "DvCompDd not found")

            cursor.execute(
                """
                UPDATE tst1a.dvcompdd1 SET 
                    projectshortname = %s,
                    comptype = %s,
                    compname = %s,
                    compsubtype = %s,
                    bkfields = %s,
                    compshortname = %s,
                    version = %s,
                    comments = %s,
                    sqltext = %s
                WHERE dvid = %s
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
                    dvid,
                ),
            )
            conn.commit()

            return response(200, "DvCompDd updated successfully")
    except Exception as e:
        return response(400, str(e))
