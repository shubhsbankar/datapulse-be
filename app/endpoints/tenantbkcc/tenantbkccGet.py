from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.tenantbkcc import router, auth_dependency, get_db, response


@router.get("/all")
async def get_all_tenantbkcc(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        groupname = current_user["groupname"]
        print(current_user)
        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT 
                    tenantid, bkcarea, hubname, bkcc,
                    createdate, user_email
                FROM tst1a.tenantbkcc 
                WHERE user_email LIKE %s
                ORDER BY createdate DESC
                """,
                (f"%{groupname}",)  # This appends the domain dynamically
            )
            tenantbkcc_list = []
            for record in cursor.fetchall():
                tenantbkcc_dict = {
                    "tenantid": record[0],
                    "bkcarea": record[1],
                    "hubname": record[2],
                    "bkcc": record[3],
                    "createdate": str(record[4]),
                    "user_email": record[5],
                }
                tenantbkcc_list.append(tenantbkcc_dict)
        return response(
            200, "Tenant BKCC records fetched successfully", data=tenantbkcc_list
        )
    except Exception as e:
        print(e.with_traceback())
        return response(400, str(e))
