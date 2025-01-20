from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.str import router, auth_dependency, get_db, response, StrDTO


@router.post("/create")
async def create_str(str_data: StrDTO, current_user: dict = Depends(auth_dependency)):
    print(f"Current user: {current_user}", str_data)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.str (
                    projectshortname, srctgthash, srchash,
                    tgthash, rtype, rdata, rfield, hr_exec, useremailid,
                    rtbkeys, rsbkeys
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    str_data.projectshortname,
                    str_data.srctgthash,
                    str_data.srchash,
                    str_data.tgthash,
                    str_data.rtype,
                    str_data.rdata,
                    str_data.rfield,
                    str_data.hr_exec,
                    current_user["sub"],
                    str_data.rtbkeys,
                    str_data.rsbkeys,
                ),
            )
            conn.commit()

            return response(201, "Source-target relationship created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_str(str_data: StrDTO, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in str_data.dict().items():
            if value is not None:
                print(f"{field}: {value}")

        print(
            "\n\nTest successful: Source-target relationship configuration is valid\n\n"
        )
        return response(200, "Source-target relationship test successful")

    except Exception as e:
        return response(400, str(e))
