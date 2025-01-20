from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompsg1 import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompSg1DTO,
)


@router.put("/update/{rdvid}")
async def update_dvcompsg1(
    rdvid: int, dvcompsg1: DvCompSg1DTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT rdvid FROM tst1a.dvcompsg1 WHERE rdvid = %s",
                (rdvid,),
            )
            if not cursor.fetchone():
                return response(404, "DvCompSg1 not found")

            cursor.execute(
                """
                UPDATE tst1a.dvcompsg1 SET 
                    projectshortname = %s,
                    dpname = %s,
                    dsname = %s,
                    comptype = %s,
                    compname = %s,
                    compsubtype = %s,
                    sqltext = %s,
                    tenantid = %s,
                    bkcarea = %s,
                    compshortname = %s,
                    comments = %s,
                    version = %s,
                    processtype = %s,
                    datefieldname = %s
                WHERE rdvid = %s
                """,
                (
                    dvcompsg1.projectshortname,
                    dvcompsg1.dpname,
                    dvcompsg1.dsname,
                    dvcompsg1.comptype,
                    dvcompsg1.compname,
                    dvcompsg1.compsubtype,
                    dvcompsg1.sqltext,
                    dvcompsg1.tenantid,
                    dvcompsg1.bkcarea,
                    dvcompsg1.compshortname,
                    dvcompsg1.comments,
                    dvcompsg1.version,
                    dvcompsg1.processtype,
                    dvcompsg1.datefieldname,
                    rdvid,
                ),
            )
            conn.commit()

            return response(200, "DvCompSg1 updated successfully")
    except Exception as e:
        return response(400, str(e))
