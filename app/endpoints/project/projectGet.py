from app.endpoints.project import *


@router.get("/all")
async def get_all_projects(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        print(current_user)

        with get_db() as (conn, cursor):
            cursor.execute(
                "SELECT projectid, projectshortname, projectname, coname, createdate, user_email, datastoreshortname FROM tst1a.projects WHERE groupname = %s",
                (current_user["groupname"],),
            )
            projects = cursor.fetchall()
            project_list = []
            for project in projects:
                project_dict = {
                    "projectid": project[0],
                    "projectshortname": project[1],
                    "projectname": project[2],
                    "coname": project[3],
                    "createdate": str(project[4]),
                    "user_email": project[5],
                    "datastoreshortname": project[6],
                }
                project_list.append(project_dict)
        return response(200, "Projects fetched successfully", data=project_list)
    except Exception as e:
        return response(400, str(e))


@router.get("/assign/all")
async def get_all_project_assignments(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                "SELECT assignid, useremail, projectshortname, is_active, who_added, createdate, groupname FROM tst1a.projectassignments_latest WHERE groupname = %s",
                (current_user["groupname"],),
            )
            project_assignments = cursor.fetchall()
            project_assign_list = []
            for project_assign in project_assignments:
                project_assign_dict = {
                    "assignid": project_assign[0],
                    "useremail": project_assign[1],
                    "projectshortname": project_assign[2],
                    "is_active": project_assign[3],
                    "who_added": project_assign[4],
                    "createdate": str(project_assign[5]),
                    "groupname": project_assign[6],
                }
                project_assign_list.append(project_assign_dict)

        return response(
            200, "Project assignments fetched successfully", data=project_assign_list
        )
    except Exception as e:
        return response(400, str(e))


@router.get("/assign/history")
async def get_all_project_assignments_history(
    current_user: dict = Depends(auth_dependency),
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                "SELECT assignid, useremail, projectshortname, is_active, who_added, createdate, groupname FROM tst1a.projectassignments_append WHERE groupname = %s",
                (current_user["groupname"],),
            )
            project_assignments = cursor.fetchall()
            project_assign_list = []
            for project_assign in project_assignments:
                project_assign_dict = {
                    "assignid": project_assign[0],
                    "useremail": project_assign[1],
                    "projectshortname": project_assign[2],
                    "is_active": project_assign[3],
                    "who_added": project_assign[4],
                    "createdate": str(project_assign[5]),
                    "groupname": project_assign[6],
                }
                project_assign_list.append(project_assign_dict)

        return response(
            200,
            "Project assignments history fetched successfully",
            data=project_assign_list,
        )
    except Exception as e:
        return response(400, str(e))


@router.get("/{project_id}")
async def get_project_by_id(
    project_id: int, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                "SELECT * FROM tst1a.projects WHERE projectid = %s AND groupname = %s",
                (project_id, current_user["groupname"]),
            )
            project = cursor.fetchone()
        return response(200, "Project fetched successfully", data=project)
    except Exception as e:
        return response(400, str(e))
