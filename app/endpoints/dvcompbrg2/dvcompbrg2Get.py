from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompbrg2 import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_dvcompbrg2s(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    dvid, projectshortname, comptype, compname, compsubtype, sqltext,
                    createdate, compshortname, comments, version, processtype,
                    datefieldname, user_email,hubnums,
                    hubnum, hubname, hubversion, bkfields,lnknums,
                    lnknum, lnkname, lnkversion, lnkbkfields
                FROM tst1a.dvcompbrg1
                ORDER BY createdate DESC
                """
            )
            dvcomppbrg = cursor.fetchall()
            print("Shubham dvcomppbrg", dvcomppbrg);
            dvcompbrg_list = []
            for dv in dvcomppbrg:
                dvcompbrg_dict = {
                    "dvid": dv[0],
                    "projectshortname": dv[1],
                    "comptype": dv[2],
                    "compname": dv[3],
                    "compsubtype": dv[4],
                    "sqltext": dv[5],
                    "createdate": str(dv[6]),
                    "compshortname": dv[7],
                    "comments": dv[8],
                    "version": float(dv[9]) if dv[9] else None,
                    "processtype": dv[10],
                    "datefieldname": dv[11],
                    "user_email": dv[12],
                    "hubnums": dv[13],
                    "hubnum": dv[14],
                    "hubname": dv[15],
                    "hubversion": float(dv[16]) if dv[16] else None,
                    "bkfields": dv[17],
                    "lnknums": dv[18],
                    "lnknum": dv[19],
                    "lnkname": dv[20],
                    "lnkversion": float(dv[21]) if dv[21] else None,
                    "lnkbkfields": dv[22]
                }
                dvcompbrg_list.append(dvcompbrg_dict)
        return response(200, "DvCompBrgs fetched successfully", data=dvcompbrg_list)
    except Exception as e:
        return response(400, str(e))
