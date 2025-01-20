from app.endpoints.user import *


@router.put("/update")
async def update_user(new_data: dict, current_user=Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        update_fields = []
        update_values = []

        # Only include non-empty fields in update
        if new_data.get("first_name"):
            update_fields.append("first_name")
            update_values.append(new_data["first_name"])

        if new_data.get("last_name"):
            update_fields.append("last_name")
            update_values.append(new_data["last_name"])

        if new_data.get("new_password"):
            update_fields.append("password")
            hashed_password = hashlib.sha256(
                new_data["new_password"].encode()
            ).hexdigest()
            update_values.append(hashed_password)

        if new_data.get("user_type"):
            if current_user["user_type"] != "admin":
                return response(403, "Only admins can update user roles.")
            update_fields.append("user_type")
            update_values.append(new_data["user_type"])

        if not update_fields:
            return response(400, "No valid fields to update")

        # Build dynamic update query
        set_clause = ", ".join([f"{field} = %s" for field in update_fields])
        update_values.append(new_data.get("useremail", current_user["sub"]))

        with get_db() as (conn, cursor):
            # fetch current info
            cursor.execute(
                sql.SQL(
                    "SELECT first_name, last_name, user_type, password FROM tst1a.users_latest WHERE useremail = %s"
                ),
                (new_data.get("useremail", current_user["sub"]),),
            )
            current_info = cursor.fetchone()
            if not current_info:
                return response(
                    404,
                    f"User with email {new_data.get('useremail', current_user['sub'])} not found",
                )

            query = sql.SQL(
                f"UPDATE tst1a.users_latest SET {set_clause} WHERE useremail = %s"
            )
            cursor.execute(query, update_values)
            current_password = current_info[3]
            if current_password != hashlib.sha256(new_data.get("current_password", "!").encode()).hexdigest():
                return response(401, "Current password is incorrect")
            # append to history
            cursor.execute(
                sql.SQL(
                    "INSERT INTO tst1a.users_append (useremail, first_name, last_name, user_type, who_added, groupname) VALUES (%s, %s, %s, %s, %s, %s)"
                ),
                (
                    new_data.get("useremail", current_user["sub"]),
                    new_data.get("first_name", current_info[0]),
                    new_data.get("last_name", current_info[1]),
                    new_data.get("user_type", current_info[2]),
                    current_user["sub"],
                    current_user["groupname"],
                ),
            )

            conn.commit()

            return response(200, "User updated successfully")

    except Exception as e:
        return response(400, str(e))


@router.put("/update_bulk")
async def update_bulk_users(
    users: list[UserBase], current_user=Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        if current_user["user_type"] != "admin":
            return response(403, "Only admins can update other users.")
        with get_db() as (conn, cursor):
            for user in users:
                # fetch current info
                cursor.execute(
                    sql.SQL(
                        "SELECT first_name, last_name, user_type FROM tst1a.users_latest WHERE useremail = %s"
                    ),
                    (user.useremail,),
                )
                current_info = cursor.fetchone()
                if not current_info:
                    return response(404, f"User with email {user.useremail} not found")
                if (
                    user.first_name == current_info[0]
                    and user.last_name == current_info[1]
                    and user.user_type == current_info[2]
                ):
                    continue
                query = sql.SQL(
                    "UPDATE tst1a.users_latest SET first_name = %s, last_name = %s, user_type = %s WHERE useremail = %s"
                )
                cursor.execute(
                    query,
                    (user.first_name, user.last_name, user.user_type, user.useremail),
                )
                # append to history
                cursor.execute(
                    sql.SQL(
                        "INSERT INTO tst1a.users_append (useremail, first_name, last_name, user_type, who_added, groupname) VALUES (%s, %s, %s, %s, %s, %s)"
                    ),
                    (
                        user.useremail,
                        user.first_name,
                        user.last_name,
                        user.user_type,
                        current_user["sub"],
                        current_user["groupname"],
                    ),
                )
                print("added to history")
            conn.commit()
            return response(200, "Users updated successfully")
    except Exception as e:
        return response(400, str(e))
