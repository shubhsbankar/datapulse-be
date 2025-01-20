from app.endpoints.datastore import *


@router.get("/all")
async def get_all_datastores(current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                """
                SELECT dsid, dsshortname, datastorename, dstype, url, driver, username, 
                       passwrd, tablename, is_valid, aws_iam_role, tempdir, credentials_file,
                       gcp_projectid, gcp_datasetid, gcp_tableid, sfaccount, sfdb, sfschema,
                       sfwarehouse, sfRole, bootstrap_servers, topic, schemareg_url, kkuser,
                       kksecret, kk_sasl_mechanism, kk_security_protocol, kk_sasl_jaas_config,
                       kk_ssl_endpoint_identification_algo, kk_ssl_ts_type, kk_ssl_ts_certificates,
                       kk_ssl_ts_location, kk_ssl_ts_password, kk_ssl_ks_type, kk_ssl_ks_location,
                       kk_ssl_ks_password, schemaregapikey, schemaregsecret, createdate, useremail,
                       bucketname, is_target, subdirectory
                FROM tst1a.datastores WHERE groupname = %s
                """,
                (current_user["groupname"],),
            )
            datastores = cursor.fetchall()
            datastore_list = []
            for ds in datastores:
                datastore_dict = {
                    "dsid": ds[0],
                    "dsshortname": ds[1],
                    "datastorename": ds[2],
                    "dstype": ds[3],
                    "url": ds[4],
                    "driver": ds[5],
                    "username": ds[6],
                    "passwrd": ds[7],
                    "tablename": ds[8],
                    "is_valid": ds[9],
                    "aws_iam_role": ds[10],
                    "tempdir": ds[11],
                    "credentials_file": ds[12],
                    "gcp_projectid": ds[13],
                    "gcp_datasetid": ds[14],
                    "gcp_tableid": ds[15],
                    "sfaccount": ds[16],
                    "sfdb": ds[17],
                    "sfschema": ds[18],
                    "sfwarehouse": ds[19],
                    "sfRole": ds[20],
                    "bootstrap_servers": ds[21],
                    "topic": ds[22],
                    "schemareg_url": ds[23],
                    "kkuser": ds[24],
                    "kksecret": ds[25],
                    "kk_sasl_mechanism": ds[26],
                    "kk_security_protocol": ds[27],
                    "kk_sasl_jaas_config": ds[28],
                    "kk_ssl_endpoint_identification_algo": ds[29],
                    "kk_ssl_ts_type": ds[30],
                    "kk_ssl_ts_certificates": ds[31],
                    "kk_ssl_ts_location": ds[32],
                    "kk_ssl_ts_password": ds[33],
                    "kk_ssl_ks_type": ds[34],
                    "kk_ssl_ks_location": ds[35],
                    "kk_ssl_ks_password": ds[36],
                    "schemaregapikey": ds[37],
                    "schemaregsecret": ds[38],
                    "createdate": str(ds[39]),
                    "useremail": ds[40],
                    "bucketname": ds[41],
                    "is_target": ds[42],
                    "subdirectory": ds[43],
                }
                datastore_list.append(datastore_dict)
        return response(200, "Datastores fetched successfully", data=datastore_list)
    except Exception as e:
        return response(400, str(e))


@router.get("/datastore/{dsid}")
async def get_datastore_by_id(dsid: int, current_user: dict = Depends(auth_dependency)):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        with get_db() as (conn, cursor):
            cursor.execute(
                "SELECT * FROM tst1a.datastores WHERE dsid = %s AND groupname = %s",
                (dsid, current_user["groupname"]),
            )
            datastore = cursor.fetchone()
            if not datastore:
                return response(404, "Datastore not found")

        return response(200, "Datastore fetched successfully", data=datastore)
    except Exception as e:
        return response(400, str(e))
