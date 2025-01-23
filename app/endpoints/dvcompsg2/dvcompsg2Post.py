from fastapi import Depends
from fastapi.responses import JSONResponse
from app.endpoints.dvcompsg2 import (
    router,
    auth_dependency,
    get_db,
    response,
    DvCompSg2DTO,
)
from fastapi.encoders import jsonable_encoder
from app.db import get_sqlalchemy_conn
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from typing import Any
from sqlalchemy.sql import text

@router.post("/create")
async def create_dvcompsg2(
    dvcompsg2: DvCompSg2DTO, current_user: dict = Depends(auth_dependency)
):
    print(dvcompsg2)
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
               """
                INSERT INTO tst1a.dvcompddl1 (
                    projectshortname, comptype,
                    compname, compsubtype, sqltext, 
                    compshortname, user_email, comments,
                    version
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    dvcompsg2.projectshortname,
                    dvcompsg2.comptype,
                    dvcompsg2.compname,
                    dvcompsg2.compsubtype,
                    dvcompsg2.sqltext,
                    dvcompsg2.compshortname,
                    current_user["sub"],
                    dvcompsg2.comments,
                    dvcompsg2.version,
                ),
            )
            conn.commit()

            return response(201, "DvCompSg2 created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/test")
async def test_dvcompsg2(
    dvcompsg2: DvCompSg2DTO, current_user: dict = Depends(auth_dependency)
) -> Any:
    try:
        # Check if the `current_user` is a JSONResponse
        if isinstance(current_user, JSONResponse):
            return current_user

        # Print non-None fields from `dvcompsg2` for debugging
        for field, value in dvcompsg2.dict().items():
            if value is not None:
                print(f"{field}: {value}")

        # Retrieve the SQL query text
        filter_query = dvcompsg2.sqltext.strip()
        print("filter_query:", filter_query)

        # Establish SQLAlchemy connection
        conn = get_sqlalchemy_conn()

        # Convert query to lowercase for validation
        query_lower = filter_query.lower()

        # Handle SELECT queries
        if query_lower.startswith("select"):
            # Execute the query and fetch results into a Pandas DataFrame
            df = pd.read_sql(filter_query, conn)
            print("Query Result DataFrame:\n", df)

            if df.empty:
                return response(404, "Dataset not found.")

            # Prepare headers and rows for the response
            headers = jsonable_encoder(df.columns.tolist())
            rows = jsonable_encoder(df.values.tolist())

            return response(
                200,
                "Test connection successful!",
                data={"headers": headers, "rows": rows},
            )

        # Handle CREATE queries
        elif query_lower.startswith("create"):
            # Execute the CREATE statement
            with conn.begin():  # Use a transaction to execute the CREATE statement
                conn.execute(text(filter_query))

            return response(201, "Table or schema created successfully.",data = {})

        else:
            # If query is neither SELECT nor CREATE, return an error response
            return response(400, "Only SELECT and CREATE queries are allowed.")

    except SQLAlchemyError as e:
        # Handle SQLAlchemy-related exceptions
        return response(400, f"Database error: {str(e)}")
    except Exception as e:
        # Handle other exceptions
        return response(400, f"Error: {str(e)}")
    
@router.post("/get-columns")
async def get_table_columns(data: dict, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        print("data:\n\n")
        for field, value in data.items():
            print(f"{field}: {value}")
            

        with get_db() as (conn, cursor):
            # Use pandas to get column information
            # query = f"SELECT * FROM tst1a.datasets"
            query = data['sqltext']
            print("query : ", query)
            df = pd.read_sql(query, conn)
            columns = df.columns.tolist()
            print("columns : ", columns)
            return response(200, "Columns fetched successfully", data=columns)
            
    except SQLAlchemyError as e:
        # Handle SQLAlchemy-related exceptions
        return response(400, f"Database error: {str(e)}")
    except Exception as e:
        return response(400, str(e))
