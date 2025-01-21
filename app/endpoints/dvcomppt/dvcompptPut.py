from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcomppt import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompPtDTO,
)


@router.put("/update/{dvid}")
async def update_dvcomppt(
    dvid: int, dvcomppt: DvCompPtDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT dvid FROM tst1a.dvcomppt1 WHERE dvid = %s",
                (dvid,),
            )
            if not cursor.fetchone():
                return response(404, "DvCompPt not found")

            cursor.execute(
                """
                UPDATE tst1a.dvcomppt1 SET 
                    projectshortname = %s,
                    comptype = %s,
                    compname = %s,
                    compsubtype = %s,
                    compshortname = %s,
                    comments = %s,
                    version = %s,
                    dhname = %s,
                    satlnums = %s,
                    satlnum = %s,
                    satlversion = %s,
                    satlname = %s,
                WHERE dvid = %s
                """,
                (
                    dvcomppt.projectshortname,
                    dvcomppt.comptype,
                    dvcomppt.compname,
                    dvcomppt.compsubtype,
                    dvcomppt.compshortname,
                    dvcomppt.comments,
                    dvcomppt.version,
                    dvcomppt.dhname,
                    dvcomppt.satlnums,
                    dvcomppt.satlnum,
                    dvcomppt.satlversion,
                    dvcomppt.satlname,
                    dvid,
                ),
            )
            conn.commit()

            return response(200, "DvCompPt updated successfully")
    except Exception as e:
        return response(400, str(e))
