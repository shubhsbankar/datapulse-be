from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rs import router, auth_dependency, get_db, response, RsDTO


@router.put("/update/{srchashid}")
async def update_rs(
    srchashid: int, rs: RsDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT srchashid FROM tst1a.rs WHERE srchashid = %s",
                (srchashid,),
            )
            if not cursor.fetchone():
                return response(404, "Source hash record not found")

            cursor.execute(
                """
                UPDATE tst1a.rs SET 
                    projectshortname = %s,
                    srcdphash = %s,
                    srcdataset = %s,
                    srctabfields = %s,
                    srchashcol = %s,
                    dpname = %s,
                    bkeys = %s,
                    bkey1 = %s,
                    bkey2 = %s,
                    bkey3 = %s,
                    bkey4 = %s,
                    bkey5 = %s,
                    bkey6 = %s,
                    bkey7 = %s,
                    bkey8 = %s,
                    bkey9 = %s,
                    bkey10 = %s
                WHERE srchashid = %s
                """,
                (
                    rs.projectshortname,
                    rs.srcdphash,
                    rs.srcdataset,
                    rs.srctabfields,
                    rs.srchashcol,
                    rs.dpname,
                    rs.bkeys,
                    rs.bkey1,
                    rs.bkey2,
                    rs.bkey3,
                    rs.bkey4,
                    rs.bkey5,
                    rs.bkey6,
                    rs.bkey7,
                    rs.bkey8,
                    rs.bkey9,
                    rs.bkey10,
                    srchashid,
                ),
            )
            conn.commit()

            return response(200, "Source hash record updated successfully")
    except Exception as e:
        return response(400, str(e))
