from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompsg1b import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompSg1DTO,
)


@router.put("/update/{rdvid}")
async def update_dvcompsg1b(
    rdvid: int, dvcompsg1b: DvCompSg1DTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT rdvid FROM tst1a.dvcompsg1b WHERE rdvid = %s",
                (rdvid,),
            )
            if not cursor.fetchone():
                return response(404, "DvCompSg1 not found")

            cursor.execute(
                """
                UPDATE tst1a.dvcompsg1b SET 
                    projectshortname = %s,
                    comptype = %s,
                    compname = %s,
                    compsubtype = %s,
                    sqltext = %s,
                    tenantid = %s,
                    bkcarea = %s,
                    compshortname = %s,
                    comments = %s,
                WHERE rdvid = %s
                """,
                (
                    dvcompsg1b.projectshortname,
                    dvcompsg1b.comptype,
                    dvcompsg1b.compname,
                    dvcompsg1b.compsubtype,
                    dvcompsg1b.sqltext,
                    dvcompsg1b.tenantid,
                    dvcompsg1b.bkcarea,
                    dvcompsg1b.compshortname,
                    dvcompsg1b.comments,
                    rdvid,
                ),
            )
            conn.commit()

            return response(200, "DvCompSg1 updated successfully")
    except Exception as e:
        return response(400, str(e))
