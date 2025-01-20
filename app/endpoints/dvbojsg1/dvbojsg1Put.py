from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvbojsg1 import (
    router,
    auth_dependency,
    get_db,
    response,
    DvBojSg1DTO,
)


@router.put("/update/{rdvid}")
async def update_dvbojsg1(
    rdvid: int, dvbojsg1: DvBojSg1DTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT rdvid FROM tst1a.dvbojsg1 WHERE rdvid = %s",
                (rdvid,),
            )
            if not cursor.fetchone():
                return response(404, "DvBojSg1 not found")

            cursor.execute(
                """
                UPDATE tst1a.dvbojsg1 SET 
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
                    dvbojsg1.projectshortname,
                    dvbojsg1.dpname,
                    dvbojsg1.dsname,
                    dvbojsg1.comptype,
                    dvbojsg1.compname,
                    dvbojsg1.compsubtype,
                    dvbojsg1.sqltext,
                    dvbojsg1.tenantid,
                    dvbojsg1.bkcarea,
                    dvbojsg1.compshortname,
                    dvbojsg1.comments,
                    dvbojsg1.version,
                    dvbojsg1.processtype,
                    dvbojsg1.datefieldname,
                    rdvid,
                ),
            )
            conn.commit()

            return response(200, "DvBojSg1 updated successfully")
    except Exception as e:
        return response(400, str(e))
