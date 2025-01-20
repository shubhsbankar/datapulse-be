from app.endpoints.auth import *


@router.patch("/update-password")
async def update_password(
    user: UserLogin, current_user: User = Depends(auth_dependency)
):
    try:
        if current_user.useremail != user.useremail:
            return response(403, "Forbidden")

        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        with get_db() as (conn, cursor):
            query = sql.SQL(
                "UPDATE tst1a.users_latest SET password = %s WHERE useremail = %s"
            )
            cursor.execute(query, (hashed_password, user.useremail))
            conn.commit()
            return response(200, "Password updated successfully")
    except Exception as e:
        return response(400, str(e))
