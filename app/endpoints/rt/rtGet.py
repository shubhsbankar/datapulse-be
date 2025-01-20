from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rt import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_rt(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    tgthashid, projectshortname, tgtdphash, tgtdataset,
                    tgttabfields, tgthashcol, dpname, bkeys,
                    bkey1, bkey2, bkey3, bkey4, bkey5,
                    bkey6, bkey7, bkey8, bkey9, bkey10,
                    createdate, useremailid, datastoreshortname, tablename
                FROM tst1a.rt 
                ORDER BY createdate DESC
                """
            )
            rt_list = []
            for rt in cursor.fetchall():
                rt_dict = {
                    "tgthashid": rt[0],
                    "projectshortname": rt[1],
                    "tgtdphash": rt[2],
                    "tgtdataset": rt[3],
                    "tgttabfields": rt[4],
                    "tgthashcol": rt[5],
                    "dpname": rt[6],
                    "bkeys": rt[7],
                    "bkey1": rt[8],
                    "bkey2": rt[9],
                    "bkey3": rt[10],
                    "bkey4": rt[11],
                    "bkey5": rt[12],
                    "bkey6": rt[13],
                    "bkey7": rt[14],
                    "bkey8": rt[15],
                    "bkey9": rt[16],
                    "bkey10": rt[17],
                    "createdate": str(rt[18]),
                    "useremailid": rt[19],
                    "datastoreshortname": rt[20],
                    "tablename": rt[21],
                }
                rt_list.append(rt_dict)
        return response(200, "Target hash records fetched successfully", data=rt_list)
    except Exception as e:
        return response(400, str(e))
