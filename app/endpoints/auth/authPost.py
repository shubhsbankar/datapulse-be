from app.endpoints.auth import *


@router.post("/signup")
async def signup_user(user: User):
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    try:
        groupname = user.useremail.split("@")[1]

        # Check if user already exists
        with get_db() as (conn, cursor):
            check_query = sql.SQL(
                "SELECT useremail FROM tst1a.users_latest WHERE useremail = %s"
            )
            cursor.execute(check_query, (user.useremail,))
            existing_user = cursor.fetchone()

            if existing_user:
                return response(400, "User with this email already exists")

        with get_db() as (conn, cursor):
            # create admin if not exists
            query = sql.SQL("SELECT * FROM tst1a.users_latest WHERE useremail = %s")
            cursor.execute(query,(f"admin@{groupname}",))
            admin_user = cursor.fetchone()
            if not admin_user:
                cursor.execute(
                    "INSERT INTO tst1a.user_groups (groupname) VALUES (%s)", (groupname,)
                )
                query = sql.SQL(
                    """
                    INSERT INTO tst1a.users_latest (useremail, password, first_name, last_name, user_type, who_added, createdate, groupname)
                    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
                    """
                )
                cursor.execute(
                    query,
                    (
                        f"admin@{groupname}",
                        hashlib.sha256("admin".encode()).hexdigest(),
                        "Admin",
                        "Admin",
                        "admin",
                        "system",
                        groupname,
                    ),
                )

            query = sql.SQL(
                """
                INSERT INTO tst1a.users_latest (useremail, password, first_name, last_name, user_type, who_added, createdate, groupname, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)
                """
            )
            cursor.execute(
                query,
                (
                    user.useremail,
                    hashed_password,
                    user.first_name,
                    user.last_name,
                    user.user_type,
                    user.who_added,
                    groupname,
                    # yes if admin is active
                    admin_user[9] if admin_user else "no",
                ),
            )
            # append to history
            cursor.execute(
                "INSERT INTO tst1a.users_append (useremail, first_name, last_name, user_type, who_added, groupname, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    user.useremail,
                    user.first_name,
                    user.last_name,
                    user.user_type,
                    user.who_added,
                    groupname,
                    admin_user[9] if admin_user else "no",
                ),
            )

            conn.commit()

            return response(200, "User created successfully!")
    except Exception as e:
        # If there's an error, roll back the transaction
        print(e.with_traceback())
        conn.rollback()
        return response(400, str(e))


@router.post("/login")
async def login_user(user: UserLogin):
    try:
        with get_db() as (conn, cursor):
            query = sql.SQL(
                "SELECT password, first_name, last_name, user_type, is_active FROM tst1a.users_latest WHERE useremail = %s"
            )
            cursor.execute(query, (user.useremail,))
            user_data = cursor.fetchone()

            print(user_data, "user_data Shubham")
            if not user_data:
                return response(401, "Invalid credentials")
            password, first_name, last_name, user_type, is_active = user_data
            print(hashlib.sha256(user.password.encode()).hexdigest())
            if password != hashlib.sha256(user.password.encode()).hexdigest():
                return response(401, "Invalid credentials")
            if not is_active:
                return response(401, "User is not active")
            print("Vaibhav 1")
            token = jwt.encode(
                {
                    "sub": user.useremail,
                    "user_type": user_type,
                    "groupname": user.useremail.split("@")[1],
                    "exp": datetime.utcnow() + timedelta(hours=12),
                },
                JWT_SECRET,
                algorithm="HS256",
            )
            print("Vaibhav 2")
            data = {
                "useremail": user.useremail,
                "first_name": first_name,
                "groupname": user.useremail.split("@")[1],
                "last_name": last_name,
                "user_type": user_type,
            }
            print("Hi Shubham", data)
            return response(200, "Login successful", token=token, data=data)

    except Exception as e:
        # print(e.with_traceback())
        return response(400, str(e))
