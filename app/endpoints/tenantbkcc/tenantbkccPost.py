from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.tenantbkcc import (
    router,
    auth_dependency,
    get_db,
    response,
    TenantBkccDTO,
)


@router.post("/create")
async def create_tenantbkcc(
    tenantbkcc: TenantBkccDTO, current_user: dict = Depends(auth_dependency)
):
    print(tenantbkcc)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.tenantbkcc (
                    tenantid, bkcarea, hubname, bkcc,
                    user_email
                ) VALUES (
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    tenantbkcc.tenantid,
                    tenantbkcc.bkcarea,
                    tenantbkcc.hubname,
                    tenantbkcc.bkcarea,
                    current_user["sub"],
                ),
            )
            conn.commit()

            return response(201, "Tenant BKCC record created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_tenantbkcc(
    tenantbkcc: TenantBkccDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in tenantbkcc.dict().items():
            if value is not None:
                print(f"{field}: {value}")

        print("\n\nTest successful: Tenant BKCC configuration is valid\n\n")
        return response(200, "Tenant BKCC test successful")

    except Exception as e:
        return response(400, str(e))
