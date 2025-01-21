from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompsg2 import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompSg2DTO,
)


@router.put("/update/{rdvid}")
async def update_dvcompsg2(
    rdvid: int, dvcompsg2: DvCompSg2DTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT dvid FROM tst1a.dvcompddl1 WHERE dvid = %s",
                (rdvid,),
            )
            if not cursor.fetchone():
                return response(404, "DvCompSg1 not found")

            cursor.execute(
                """
                UPDATE tst1a.dvcompddl1 SET 
                    projectshortname = %s,
                    comptype = %s,
                    compname = %s,
                    compsubtype = %s,
                    sqltext = %s,
                    compshortname = %s,
                    comments = %s,
                    version = %s,
                WHERE dvid = %s
                """,
                (
                    dvcompsg2.projectshortname,
                    dvcompsg2.comptype,
                    dvcompsg2.compname,
                    dvcompsg2.compsubtype,
                    dvcompsg2.sqltext,
                    dvcompsg2.compshortname,
                    dvcompsg2.comments,
                    dvcompsg2.version,
                    rdvid,
                ),
            )
            conn.commit()

            return response(200, "DvCompSg2 updated successfully")
    except Exception as e:
        return response(400, str(e))
