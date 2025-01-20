from app.endpoints.datastore import *


@router.put("/update/{dsid}")
async def update_datastore(
    dsid: int, datastore: Datastore, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        if current_user["user_type"] != "admin":
            return response(403, "You are not authorized to update a datastore")

        with get_db() as (conn, cursor):
            # Check if datastore exists and belongs to user's group
            cursor.execute(
                "SELECT * FROM tst1a.datastores WHERE dsid = %s AND groupname = %s",
                (dsid, current_user["groupname"]),
            )
            if not cursor.fetchone():
                return response(404, "Datastore not found")

            # Update the datastore
            cursor.execute(
                """
                UPDATE tst1a.datastores SET 
                    dsshortname = %s,
                    datastorename = %s,
                    dstype = %s,
                    url = %s,
                    driver = %s,
                    username = %s,
                    passwrd = %s,
                    tablename = %s,
                    is_valid = %s,
                    aws_iam_role = %s,
                    tempdir = %s,
                    credentials_file = %s,
                    gcp_projectid = %s,
                    gcp_datasetid = %s,
                    gcp_tableid = %s,
                    sfaccount = %s,
                    sfdb = %s,
                    sfschema = %s,
                    sfwarehouse = %s,
                    sfRole = %s,
                    bootstrap_servers = %s,
                    topic = %s,
                    schemareg_url = %s,
                    kkuser = %s,
                    kksecret = %s,
                    kk_sasl_mechanism = %s,
                    kk_security_protocol = %s,
                    kk_sasl_jaas_config = %s,
                    kk_ssl_endpoint_identification_algo = %s,
                    kk_ssl_ts_type = %s,
                    kk_ssl_ts_certificates = %s,
                    kk_ssl_ts_location = %s,
                    kk_ssl_ts_password = %s,
                    kk_ssl_ks_type = %s,
                    kk_ssl_ks_location = %s,
                    kk_ssl_ks_password = %s,
                    schemaregapikey = %s,
                    schemaregsecret = %s
                WHERE dsid = %s
                """,
                (
                    datastore.dsshortname,
                    datastore.datastorename,
                    datastore.dstype,
                    datastore.url,
                    datastore.driver,
                    datastore.username,
                    datastore.passwrd,
                    datastore.tablename,
                    datastore.is_valid,
                    datastore.aws_iam_role,
                    datastore.tempdir,
                    datastore.credentials_file,
                    datastore.gcp_projectid,
                    datastore.gcp_datasetid,
                    datastore.gcp_tableid,
                    datastore.sfaccount,
                    datastore.sfdb,
                    datastore.sfschema,
                    datastore.sfwarehouse,
                    datastore.sfRole,
                    datastore.bootstrap_servers,
                    datastore.topic,
                    datastore.schemareg_url,
                    datastore.kkuser,
                    datastore.kksecret,
                    datastore.kk_sasl_mechanism,
                    datastore.kk_security_protocol,
                    datastore.kk_sasl_jaas_config,
                    datastore.kk_ssl_endpoint_identification_algo,
                    datastore.kk_ssl_ts_type,
                    datastore.kk_ssl_ts_certificates,
                    datastore.kk_ssl_ts_location,
                    datastore.kk_ssl_ts_password,
                    datastore.kk_ssl_ks_type,
                    datastore.kk_ssl_ks_location,
                    datastore.kk_ssl_ks_password,
                    datastore.schemaregapikey,
                    datastore.schemaregsecret,
                    dsid,
                ),
            )
            conn.commit()
        return response(200, "Datastore updated successfully")
    except Exception as e:
        return response(400, str(e))
