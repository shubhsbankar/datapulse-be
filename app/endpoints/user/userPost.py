from typing import List
from fastapi import UploadFile
from fastapi.params import File, Path
import ldap3
from app.endpoints.user import *
from app.utils.constants import get_project_paths
from fastapi import APIRouter, Depends, Query


# LDAP_SERVER = "ldap://localhost:389"
# BASE_DN = "dc=example,dc=com"
# ALLOWED_DOMAINS = ["example.com", "office.com"]


@router.post("/ldap/pull")
async def pull_ldap_users(config: LDAPConfig):
    ldap_server = ldap3.Server(config.ldap_url)
    admin_dn = config.admin_dn
    ldap_conn = ldap3.Connection(
        ldap_server, user=admin_dn, password=config.ldap_password
    )

    if not ldap_conn.bind():
        return {"error": f"Failed to bind: {ldap_conn.result}"}

    # Change the search parameters to match your LDAP structure
    search_base = (
        "ou=user,dc=example,dc=com"  # Adjust this to match your LDAP structure
    )
    search_filter = "(objectClass=inetOrgPerson)"
    attributes = ["cn", "sn", "mail", "uid"]

    ldap_conn.search(
        search_base=search_base, search_filter=search_filter, attributes=attributes
    )
    print(ldap_conn.entries)

    # Extract user data into a clean dictionary
    users = [
        {"useremail": entry.mail.value, "first_name": entry.cn.value}
        for entry in ldap_conn.entries
    ]
    return response(200, "LDAP users retrieved successfully", data=users)


@router.post("/create_bulk")
async def create_bulk_users(users: List[User], current_user=Depends(auth_dependency)):
    if isinstance(current_user, JSONResponse):
        return current_user

    for user in users:
        user.password = hashlib.sha256(user.password.encode()).hexdigest()
    try:
        with get_db() as (conn, cursor):
            cursor.execute(
                "INSERT INTO tst1a.users_latest (useremail, password, first_name, last_name, user_type, who_added, groupname) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    user.useremail,
                    user.password,
                    user.first_name,
                    user.last_name,
                    user.user_type,
                    current_user["sub"],
                    current_user["groupname"],
                ),
            )
            # append to history
            cursor.execute(
                "INSERT INTO tst1a.users_append (useremail, first_name, last_name, user_type, who_added, groupname) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    user.useremail,
                    user.first_name,
                    user.last_name,
                    user.user_type,
                    current_user["sub"],
                    current_user["groupname"],
                ),
            )
            conn.commit()
            
    except Exception as e:
        return response(400, e)
    return response(201, "Users created successfully")


@router.post("/upload_csv/{tablename}")
async def upload_csv(file: UploadFile = File(...), tablename: str = Path(...), project_shortname: str = Query(None), current_user=Depends(auth_dependency)):
    # write file to disk
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    try:
        print(file.filename, tablename, file.file, project_shortname, current_user, file_path)
        # df = pd.read_csv(file.file)
        # print(df)
        
        # with get_db() as (conn, cursor):
        #     # Create table if not exists
        #     cursor.execute(f"CREATE TABLE IF NOT EXISTS {tablename} ({', '.join([f'{col} TEXT' for col in df.columns])})")
            
        #     # Insert data
        #     values = [tuple(row) for row in df.values]
        #     placeholders = ", ".join(["%s"] * len(df.columns))
        #     insert_query = f"INSERT INTO {tablename} VALUES ({placeholders})"
        #     print(insert_query, values)
        #     cursor.executemany(insert_query, values)
            
        #     conn.commit()

        return response(201, f"CSV uploaded successfully to {tablename}")
    except Exception as e:
        return response(400, e)
