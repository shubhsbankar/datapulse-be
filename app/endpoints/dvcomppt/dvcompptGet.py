from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcomppt import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_dvcomppts(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    dvid, projectshortname, comptype, compname, compsubtype, 
                    createdate, compshortname,
                    user_email, comments, version, 
                    dhname,satlnums,satlnum,satlname,satlversion
                FROM tst1a.dvcomppt 
                ORDER BY createdate DESC
                """
            )
            dvcomppts = cursor.fetchall()
            print("dvcomppts", dvcomppts);
            dvcomppt_list = []
            for dv in dvcomppts:
                dvcomppt_dict = {
                    "dvid": dv[0],
                    "projectshortname": dv[1],
                    "comptype": dv[2],
                    "compname": dv[3],
                    "compsubtype": dv[4],
                    "createdate": str(dv[5]),
                    "compshortname": dv[6],
                    "user_email": dv[7],
                    "comments": dv[8],
                    "version": float(dv[9]) if dv[9] else None,
                    "dhname" : dv[10],
                    "satlnums" : dv[11],
                    "satlnum":dv[12],
                    "satlname": dv[13],
                    "satlversion":float(dv[14]) if dv[14] else None

                }
                dvcomppt_list.append(dvcomppt_dict)
        return response(200, "DvCompPts fetched successfully", data=dvcomppt_list)
    except Exception as e:
        return response(400, str(e))
