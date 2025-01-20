from app.endpoints.project import *


@router.put("project/{project_id}")
async def update_project(
    project_id: int, project: ProjectBase, current_user: dict = Depends(auth_dependency)
):
    if isinstance(current_user, JSONResponse):
        return current_user

    if current_user["user_type"] != "admin":
        return response(403, "You are not authorized to update a project")

    with get_db() as (conn, cursor):
        cursor.execute(
            "UPDATE tst1a.projects SET projectshortname = %s, projectname = %s, coname = %s WHERE projectid = %s",
            (project.projectshortname, project.projectname, project.coname, project_id),
        )
        conn.commit()

    return response(200, "Project updated successfully")


@router.put("/assign/{assign_id}")
async def update_project_assign(
    assign_id: int,
    new_data: ProjectAssignUpdate,
    current_user: dict = Depends(auth_dependency),
):
    if isinstance(current_user, JSONResponse):
        return current_user

    if current_user["user_type"] != "admin":
        return response(403, "You are not authorized to update a project assignment")

    with get_db() as (conn, cursor):

        cursor.execute(
            "UPDATE tst1a.projectassignments_latest SET is_active = %s WHERE assignid = %s",
            (new_data.is_active, assign_id),
        )
        # add to history table
        cursor.execute(
            "SELECT useremail, projectshortname FROM tst1a.projectassignments_latest WHERE assignid = %s",
            (assign_id,),
        )
        useremail, projectshortname = cursor.fetchone()
        cursor.execute(
            "INSERT INTO tst1a.projectassignments_append (useremail, projectshortname, is_active, who_added, groupname) VALUES (%s, %s, %s, %s, %s)",
            (
                useremail,
                projectshortname,
                new_data.is_active,
                current_user["sub"],
                current_user["groupname"],
            ),
        )
        conn.commit()
    return response(200, "Project assignment updated successfully")
