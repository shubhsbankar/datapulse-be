from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rt import router, auth_dependency, get_db, response, RtDTO


@router.put("/update/{tgthashid}")
async def update_rt(
    tgthashid: int, rt: RtDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                "SELECT tgthashid FROM tst1a.rt WHERE tgthashid = %s",
                (tgthashid,),
            )
            if not cursor.fetchone():
                return response(404, "Target hash record not found")

            cursor.execute(
                """
                UPDATE tst1a.rt SET 
                    projectshortname = %s,
                    tgtdphash = %s,
                    tgtdataset = %s,
                    tgttabfields = %s,
                    tgthashcol = %s,
                    dpname = %s,
                    datastoreshortname = %s,
                    tablename = %s,
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
                WHERE tgthashid = %s
                """,
                (
                    rt.projectshortname,
                    rt.tgtdphash,
                    rt.tgtdataset,
                    rt.tgttabfields,
                    rt.tgthashcol,
                    rt.dpname,
                    rt.datastoreshortname,
                    rt.tablename,
                    rt.bkeys,
                    rt.bkey1,
                    rt.bkey2,
                    rt.bkey3,
                    rt.bkey4,
                    rt.bkey5,
                    rt.bkey6,
                    rt.bkey7,
                    rt.bkey8,
                    rt.bkey9,
                    rt.bkey10,
                    tgthashid,
                ),
            )
            conn.commit()

            return response(200, "Target hash record updated successfully")
    except Exception as e:
        return response(400, str(e))
