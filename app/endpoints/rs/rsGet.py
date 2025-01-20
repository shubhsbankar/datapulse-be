from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rs import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_rs(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    srchashid, projectshortname, srcdphash, srcdataset,
                    srctabfields, srchashcol, dpname, bkeys,
                    bkey1, bkey2, bkey3, bkey4, bkey5,
                    bkey6, bkey7, bkey8, bkey9, bkey10,
                    createdate, useremailid, datastoreshortname, tablename
                FROM tst1a.rs 
                ORDER BY createdate DESC
                """
            )
            rs_list = []
            for rs in cursor.fetchall():
                rs_dict = {
                    "srchashid": rs[0],
                    "projectshortname": rs[1],
                    "srcdphash": rs[2],
                    "srcdataset": rs[3],
                    "srctabfields": rs[4],
                    "srchashcol": rs[5],
                    "dpname": rs[6],
                    "bkeys": rs[7],
                    "bkey1": rs[8],
                    "bkey2": rs[9],
                    "bkey3": rs[10],
                    "bkey4": rs[11],
                    "bkey5": rs[12],
                    "bkey6": rs[13],
                    "bkey7": rs[14],
                    "bkey8": rs[15],
                    "bkey9": rs[16],
                    "bkey10": rs[17],
                    "createdate": str(rs[18]),
                    "useremailid": rs[19],
                    "datastoreshortname": rs[20],
                    "tablename": rs[21],
                }
                rs_list.append(rs_dict)
        return response(200, "Source hash records fetched successfully", data=rs_list)
    except Exception as e:
        return response(400, str(e))
