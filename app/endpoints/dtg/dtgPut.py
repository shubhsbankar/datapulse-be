from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dtg import router, auth_dependency, get_db, response, DtgDTO


@router.put("/update/{dtid}")
async def update_dtg(
    dtid: int, dtg: DtgDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if dtg exists
            cursor.execute(
                "SELECT dtid FROM tst1a.dtg WHERE dtid = %s",
                (dtid,),
            )
            if not cursor.fetchone():
                return response(404, "DTG not found")

            cursor.execute(
                """
                UPDATE tst1a.dtg SET 
                    dtshortname = %s,
                    chkfilename = %s,
                    datasettype = %s,
                    datasrcnum = %s,
                    projectshortname = %s,
                    datasetshortname = %s,
                    dataproductshortname = %s,
                    testcoverageversion = %s,
                    comments = %s
                WHERE dtid = %s
                """,
                (
                    dtg.dtshortname,
                    dtg.chkfilename,
                    dtg.datasettype,
                    dtg.datasrcnum,
                    dtg.projectshortname,
                    dtg.datasetshortname,
                    dtg.dataproductshortname,
                    dtg.testcoverageversion,
                    dtg.comments,
                    dtid,
                ),
            )
            conn.commit()

            return response(200, "DTG updated successfully")
    except Exception as e:
        return response(400, str(e))
