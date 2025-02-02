from app.endpoints.project import *


@router.post("/create")
async def create_project(
    project: ProjectBase, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        if current_user["user_type"] != "admin":
            return response(403, "You are not authorized to create a project")

        with get_db() as (conn, cursor):
            # check if projectshortname already exists
            cursor.execute(
                "SELECT * FROM tst1a.projects WHERE projectshortname = %s",
                (project.projectshortname,),
            )
            if cursor.fetchone():
                return response(400, "Project shortname already exists")

            cursor.execute(
                """INSERT INTO tst1a.projects 
                (projectshortname, projectname, user_email, coname, datastoreshortname, 
                groupname, sourcetype, credentials_file, accesskey, secretkey) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    project.projectshortname,
                    project.projectname,
                    current_user["sub"],
                    project.coname,
                    project.datastoreshortname,
                    current_user["groupname"],
                    project.sourcetype,
                    project.credentials_file,
                    project.accesskey,
                    project.secretkey,
                ),
            )
            conn.commit()
        return response(200, "Project created successfully")
    except Exception as e:
        return response(400, str(e))


@router.post("/assign/create")
async def assign_create(
    project_assign: ProjectAssignBase, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        if current_user["user_type"] != "admin":
            return response(403, "You are not authorized to assign a project")

        with get_db() as (conn, cursor):
            cursor.execute(
                "INSERT INTO tst1a.projectassignments_latest (useremail, projectshortname, is_active, who_added, groupname) VALUES (%s, %s, %s, %s, %s)",
                (
                    project_assign.useremail,
                    project_assign.projectshortname,
                    project_assign.is_active,
                    current_user["sub"],
                    current_user["groupname"],
                ),
            )
            # add to history table
            cursor.execute(
                "INSERT INTO tst1a.projectassignments_append (useremail, projectshortname, is_active, who_added, groupname) VALUES (%s, %s, %s, %s, %s)",
                (
                    project_assign.useremail,
                    project_assign.projectshortname,
                    project_assign.is_active,
                    current_user["sub"],
                    current_user["groupname"],
                ),
            )
            conn.commit()

        return response(200, "Project assigned successfully")
    except Exception as e:
        return response(400, str(e))
