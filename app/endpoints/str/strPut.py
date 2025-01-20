from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.str import router, auth_dependency, get_db, response, StrDTO


@router.put("/update/{srctgthashid}")
async def update_str(
    srctgthashid: int, str_data: StrDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT srctgthashid FROM tst1a.str WHERE srctgthashid = %s",
                (srctgthashid,),
            )
            if not cursor.fetchone():
                return response(404, "Source-target relationship not found")

            cursor.execute(
                """
                UPDATE tst1a.str SET 
                    projectshortname = %s,
                    srctgthash = %s,
                    srchash = %s,
                    tgthash = %s,
                    rtype = %s,
                    rdata = %s,
                    rfield = %s,
                    hr_exec = %s
                WHERE srctgthashid = %s
                """,
                (
                    str_data.projectshortname,
                    str_data.srctgthash,
                    str_data.srchash,
                    str_data.tgthash,
                    str_data.rtype,
                    str_data.rdata,
                    str_data.rfield,
                    str_data.hr_exec,
                    srctgthashid,
                ),
            )
            conn.commit()

            return response(200, "Source-target relationship updated successfully")
    except Exception as e:
        return response(400, str(e))
