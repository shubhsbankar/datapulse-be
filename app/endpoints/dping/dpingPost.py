from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dping import router, auth_dependency, get_db, response, Dping


@router.post("/create")
async def create_dping(dping: Dping, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.dping (
                    dpshortname, htmlfilename, datasettype,
                    projectshortname, datasetshortname, dataproductshortname,
                    useremailid
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    dping.dpshortname,
                    dping.htmlfilename,
                    dping.datasettype,
                    dping.projectshortname,
                    dping.datasetshortname,
                    dping.dataproductshortname,
                    current_user["sub"],
                ),
            )
            conn.commit()

            return response(201, "Dping created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_dping(dping: Dping, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None dping fields for testing
        if dping.dpid:
            print(f"Dping ID: {dping.dpid}")
        if dping.dpshortname:
            print(f"Dping Short Name: {dping.dpshortname}")
        if dping.htmlfilename:
            print(f"HTML File Name: {dping.htmlfilename}")
        if dping.datasettype:
            print(f"Dataset Type: {dping.datasettype}")
        if dping.projectshortname:
            print(f"Project Short Name: {dping.projectshortname}")
        if dping.datasetshortname:
            print(f"Dataset Short Name: {dping.datasetshortname}")
        if dping.dataproductshortname:
            print(f"Data Product Short Name: {dping.dataproductshortname}")
        if dping.createdate:
            print(f"Create Date: {dping.createdate}")
        if dping.useremailid:
            print(f"User Email ID: {dping.useremailid}")

        print("\n\nTest successful: Dping configuration is valid\n\n")
        return response(200, "Dping test successful")

    except Exception as e:
        return response(400, str(e))
