from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.tenantbkcc import (
    router,
    auth_dependency,
    get_db,
    response,
    TenantBkccDTO,
)


@router.put("/update/{tenantid}/{bkcarea}/{hubname}")
async def update_tenantbkcc(
    tenantid: str,
    bkcarea: str,
    hubname: str,
    tenantbkcc: TenantBkccDTO,
    current_user: dict = Depends(auth_dependency),
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            # First check if record exists
            cursor.execute(
                """
                SELECT tenantid 
                FROM tst1a.tenantbkcc 
                WHERE tenantid = %s AND bkcarea = %s AND hubname = %s
                """,
                (tenantid, bkcarea, hubname),
            )
            if not cursor.fetchone():
                return response(404, "Tenant BKCC record not found")

            cursor.execute(
                """
                UPDATE tst1a.tenantbkcc SET 
                    bkcc = %s,
                    user_email = %s
                WHERE tenantid = %s AND bkcarea = %s AND hubname = %s
                """,
                (tenantbkcc.bkcc, current_user["sub"], tenantid, bkcarea, hubname),
            )
            conn.commit()

            return response(200, "Tenant BKCC record updated successfully")
    except Exception as e:
        return response(400, str(e))
