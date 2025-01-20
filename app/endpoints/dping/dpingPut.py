from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dping import router, auth_dependency, get_db, response, Dping


@router.put("/update/{dpid}")
async def update_dping(
    dpid: int, dping: Dping, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if dping exists
            cursor.execute(
                "SELECT dpid FROM tst1a.dping WHERE dpid = %s",
                (dpid,),
            )
            if not cursor.fetchone():
                return response(404, "Dping not found")

            cursor.execute(
                """
                UPDATE tst1a.dping SET 
                    dpshortname = %s,
                    htmlfilename = %s,
                    datasettype = %s,
                    projectshortname = %s,
                    datasetshortname = %s,
                    dataproductshortname = %s
                WHERE dpid = %s
                """,
                (
                    dping.dpshortname,
                    dping.htmlfilename,
                    dping.datasettype,
                    dping.projectshortname,
                    dping.datasetshortname,
                    dping.dataproductshortname,
                    dpid,
                ),
            )
            conn.commit()

            return response(200, "Dping updated successfully")
    except Exception as e:
        return response(400, str(e))
