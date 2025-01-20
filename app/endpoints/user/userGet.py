from app.endpoints.user import *


@router.get("/get/all")
async def get_users(current_user=Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        if current_user["user_type"] != "admin":
            return response(403, "Forbidden")
        
        print(current_user)

        with get_db() as (conn, cursor):
            query = sql.SQL("SELECT useremail, first_name, last_name, user_type, who_added, createdate FROM tst1a.users_latest where groupname = %s")
            cursor.execute(
                query,
                (current_user["groupname"],)
            )
            users = cursor.fetchall()
            user_list = []
            for user in users:
                user_dict = {
                    "useremail": user[0],
                    "first_name": user[1],
                    "last_name": user[2],
                    "user_type": user[3],
                    "who_added": user[4],
                    "createdate": str(user[5]),
                }
                user_list.append(user_dict)
            return response(200, "Users fetched successfully", data=user_list)
    except Exception as e:
        print(e.with_traceback())
        return response(400, str(e))


@router.get("/get/all/history")
async def get_users_history(current_user=Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        
        if current_user["user_type"] != "admin":
            return response(403, "Forbidden")

        with get_db() as (conn, cursor):
            query = sql.SQL(
                "SELECT useremail, first_name, last_name, user_type, who_added, createdate FROM tst1a.users_append where groupname = %s"
            )
            cursor.execute(query, (current_user["groupname"],))
            # cursor.execute(
            #     "SELECT useremail, first_name, last_name, user_type, who_added, createdate FROM tst1a.users_append where groupname = '%s'",
            #     current_user["groupname"],
            # )
            users = cursor.fetchall()
            user_list = []
            for user in users:
                user_dict = {
                    "useremail": user[0],
                    "first_name": user[1],
                    "last_name": user[2],
                    "user_type": user[3],
                    "who_added": user[4],
                    "createdate": str(user[5]),
                }
                user_list.append(user_dict)
            return response(200, "Users history fetched successfully", data=user_list)
    except Exception as e:
        print(e.with_traceback())
        return response(400, str(e))
