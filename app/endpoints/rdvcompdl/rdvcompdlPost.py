from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.rdvcompdl import *
from app.db import get_db, get_sqlalchemy_conn
from fastapi.encoders import jsonable_encoder

@router.post("/create")
async def create_rdvcompdl(
    rdvcompdl: RdvCompDlDTO, current_user: dict = Depends(auth_dependency)
):
    print(rdvcompdl)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO tst1a.rdvcompdl (
                    projectshortname, dpname, dsname, comptype,
                    compname, compkeyname, hubnums, hubnum,
                    hubname, hubversion, bkfields, degen,
                    degenids, tenantid, bkcarea, user_email,
                    compshortname, version
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    rdvcompdl.projectshortname,
                    rdvcompdl.dpname,
                    rdvcompdl.dsname,
                    rdvcompdl.comptype,
                    rdvcompdl.compname,
                    rdvcompdl.compkeyname,
                    rdvcompdl.hubnums,
                    rdvcompdl.hubnum,
                    rdvcompdl.hubname,
                    rdvcompdl.hubversion,
                    rdvcompdl.bkfields,
                    rdvcompdl.degen,
                    rdvcompdl.degenids,
                    rdvcompdl.tenantid,
                    rdvcompdl.bkcarea,
                    current_user["sub"],
                    rdvcompdl.compshortname,
                    rdvcompdl.version,
                ),
            )
            conn.commit()

            return response(201, "RdvCompDl created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_rdvcompdl(
    rdvcompdl: RdvCompDlDTO, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields for testing
        for field, value in rdvcompdl.dict().items():
            if value is not None:
                print(f"{field}: {value}")

                filter_query = f"SELECT * FROM tst1a.users_latest"
        conn = get_sqlalchemy_conn()
        df = pd.read_sql(filter_query, conn)
        print(df)
        if df.empty:
            return response(404, "Dataset not found.")
        conn.commit()

        headers = jsonable_encoder(df.columns.tolist())
        rows = jsonable_encoder(df.values.tolist())
        if df.empty:
            return response(404, "Dataset not found.")
        conn.commit()
        return response(
            200, "Test connection successful!", data={"headers": headers, "rows": rows}
        )


        # print("\n\nTest successful: RdvCompDl configuration is valid\n\n")
        # return response(200, "RdvCompDl test successful")

    except Exception as e:
        return response(400, str(e))


@router.post("/get-bkfields")
async def get_bkfields(data: dict, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        print("data:\n\n")
        for field, value in data.items():
            print(f"{field}: {value}")

        with get_db() as (conn, cursor):
            # Use pandas to get column information
            query = f"SELECT * FROM tst1a.datasets"
            df = pd.read_sql(query, conn)
            bkfields = df.columns.tolist()
            print("bkfields",bkfields)

            return response(200, "Bkfields fetched successfully", data=bkfields)
    except Exception as e:
        return response(400, str(e))


@router.post("/get-dgenids")
async def get_dgenids(data: dict, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        print("data:\n\n")
        for field, value in data.items():
            print(f"{field}: {value}")

        with get_db() as (conn, cursor):
            query = f"SELECT DISTINCT datasetid FROM tst1a.datasets"
            df = pd.read_sql(query, conn)
            dgenids = df["datasetid"].tolist()

            return response(200, "Dgenids fetched successfully", data=dgenids)
    except Exception as e:
        return response(400, str(e))
