from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.str import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_str(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    srctgthashid, projectshortname, srctgthash,
                    srchash, tgthash, rtype, rdata, rfield,
                    hr_exec, createdate, useremailid,
                    rtbkeys, rsbkeys
                FROM tst1a.str 
                ORDER BY createdate DESC
                """
            )
            str_list = []
            for str_record in cursor.fetchall():
                str_dict = {
                    "srctgthashid": str_record[0],
                    "projectshortname": str_record[1],
                    "srctgthash": str_record[2],
                    "srchash": str_record[3],
                    "tgthash": str_record[4],
                    "rtype": str_record[5],
                    "rdata": str_record[6],
                    "rfield": str_record[7],
                    "hr_exec": str_record[8],
                    "createdate": str(str_record[9]),
                    "useremailid": str_record[10],
                    "rtbkeys": str_record[11],
                    "rsbkeys": str_record[12],
                }
                str_list.append(str_dict)
        return response(
            200, "Source-target relationships fetched successfully", data=str_list
        )
    except Exception as e:
        return response(400, str(e))
