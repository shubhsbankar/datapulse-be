from app.endpoints.datastore import *


@router.post("/create")
async def create_datastore(
    datastore: Datastore, current_user: dict = Depends(auth_dependency)
):
    print(datastore)

    try:
        if isinstance(current_user, JSONResponse):
            return current_user

        if current_user["user_type"] != "admin":
            return response(403, "You are not authorized to create a datastore")

        with get_db() as (conn, cursor):
            # Check if dsshortname already exists
            cursor.execute(
                "SELECT * FROM tst1a.datastores WHERE dsshortname = %s",
                (datastore.dsshortname,),
            )
            if cursor.fetchone():
                return response(400, "Datastore shortname already exists")

            # Set default values for optional fields
            aws_iam_role = datastore.aws_iam_role or None
            tempdir = datastore.tempdir or None
            credentials_file = datastore.credentials_file or None
            gcp_projectid = datastore.gcp_projectid or None
            gcp_datasetid = datastore.gcp_datasetid or None
            gcp_tableid = datastore.gcp_tableid or None
            bootstrap_servers = datastore.bootstrap_servers or None
            topic = datastore.topic or None
            schemareg_url = datastore.schemareg_url or None
            kkuser = datastore.kkuser or None
            kksecret = datastore.kksecret or None
            kk_sasl_mechanism = datastore.kk_sasl_mechanism or None
            kk_security_protocol = datastore.kk_security_protocol or None
            kk_sasl_jaas_config = datastore.kk_sasl_jaas_config or None
            kk_ssl_endpoint_identification_algo = (
                datastore.kk_ssl_endpoint_identification_algo or None
            )
            kk_ssl_ts_type = datastore.kk_ssl_ts_type or None
            kk_ssl_ts_certificates = datastore.kk_ssl_ts_certificates or None
            kk_ssl_ts_location = datastore.kk_ssl_ts_location or None
            kk_ssl_ts_password = datastore.kk_ssl_ts_password or None
            kk_ssl_ks_type = datastore.kk_ssl_ks_type or None
            kk_ssl_ks_location = datastore.kk_ssl_ks_location or None
            kk_ssl_ks_password = datastore.kk_ssl_ks_password or None
            schemaregapikey = datastore.schemaregapikey or None
            schemaregsecret = datastore.schemaregsecret or None
            bucketname = datastore.bucketname or None
            subdirectory = datastore.subdirectory or None
            is_target = datastore.is_target or None

            cursor.execute(
                """
                INSERT INTO tst1a.datastores (
                    dsshortname,
                    datastorename,
                    dstype,
                    url,
                    driver,
                    username,
                    passwrd,
                    tablename,
                    useremail,
                    is_valid,
                    aws_iam_role,
                    tempdir,
                    credentials_file,
                    gcp_projectid,
                    gcp_datasetid,
                    gcp_tableid,
                    sfaccount,
                    sfdb,
                    sfschema,
                    sfwarehouse,
                    sfRole,
                    bootstrap_servers,
                    topic,
                    schemareg_url,
                    kkuser,
                    kksecret,
                    kk_sasl_mechanism,
                    kk_security_protocol,
                    kk_sasl_jaas_config,
                    kk_ssl_endpoint_identification_algo,
                    kk_ssl_ts_type,
                    kk_ssl_ts_certificates,
                    kk_ssl_ts_location,
                    kk_ssl_ts_password,
                    kk_ssl_ks_type,
                    kk_ssl_ks_location,
                    kk_ssl_ks_password,
                    schemaregapikey,
                    schemaregsecret,
                    bucketname,
                    subdirectory,
                    is_target,
                    groupname
                    )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s
                )
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
                    current_user["sub"],
                    datastore.is_valid,
                    aws_iam_role,
                    tempdir,
                    credentials_file,
                    gcp_projectid,
                    gcp_datasetid,
                    gcp_tableid,
                    datastore.sfaccount,
                    datastore.sfdb,
                    datastore.sfschema,
                    datastore.sfwarehouse,
                    datastore.sfRole,
                    bootstrap_servers,
                    topic,
                    schemareg_url,
                    kkuser,
                    kksecret,
                    kk_sasl_mechanism,
                    kk_security_protocol,
                    kk_sasl_jaas_config,
                    kk_ssl_endpoint_identification_algo,
                    kk_ssl_ts_type,
                    kk_ssl_ts_certificates,
                    kk_ssl_ts_location,
                    kk_ssl_ts_password,
                    kk_ssl_ks_type,
                    kk_ssl_ks_location,
                    kk_ssl_ks_password,
                    schemaregapikey,
                    schemaregsecret,
                    bucketname,
                    subdirectory,
                    is_target,
                    current_user["groupname"],
                ),
            )
            conn.commit()
        return response(200, "Datastore created successfully")
    except Exception as e:
        print(e)
        return response(400, str(e))


@router.post("/test")
async def test_datastore_connection(
    datastore: Datastore, current_user: dict = Depends(auth_dependency)
):
    try:
        if isinstance(current_user, JSONResponse):
            return current_user
        if datastore.dsshortname:
            print(f"Datastore Shortname: {datastore.dsshortname}")
        if datastore.datastorename:
            print(f"Datastore Name: {datastore.datastorename}")
        if datastore.dstype:
            print(f"Datastore Type: {datastore.dstype}")
        if datastore.url:
            print(f"Datastore URL: {datastore.url}")
        if datastore.driver:
            print(f"Datastore Driver: {datastore.driver}")
        if datastore.username:
            print(f"Datastore Username: {datastore.username}")
        if datastore.passwrd:
            print(f"Datastore Password: {datastore.passwrd}")
        if datastore.tablename:
            print(f"Datastore Table Name: {datastore.tablename}")
        # Print non-None datastore fields
        if datastore.aws_iam_role:
            print(f"AWS IAM Role: {datastore.aws_iam_role}")
        if datastore.tempdir:
            print(f"Temp Directory: {datastore.tempdir}")
        if datastore.credentials_file:
            print(f"Credentials File: {datastore.credentials_file}")
        if datastore.createdate:
            print(f"Create Date: {datastore.createdate}")
        if datastore.gcp_projectid:
            print(f"GCP Project ID: {datastore.gcp_projectid}")
        if datastore.gcp_datasetid:
            print(f"GCP Dataset ID: {datastore.gcp_datasetid}")
        if datastore.gcp_tableid:
            print(f"GCP Table ID: {datastore.gcp_tableid}")
        if datastore.sfaccount:
            print(f"Snowflake Account: {datastore.sfaccount}")
        if datastore.sfdb:
            print(f"Snowflake DB: {datastore.sfdb}")
        if datastore.sfschema:
            print(f"Snowflake Schema: {datastore.sfschema}")
        if datastore.sfwarehouse:
            print(f"Snowflake Warehouse: {datastore.sfwarehouse}")
        if datastore.sfRole:
            print(f"Snowflake Role: {datastore.sfRole}")
        if datastore.bootstrap_servers:
            print(f"Bootstrap Servers: {datastore.bootstrap_servers}")
        if datastore.topic:
            print(f"Topic: {datastore.topic}")
        if datastore.schemareg_url:
            print(f"Schema Registry URL: {datastore.schemareg_url}")
        if datastore.kkuser:
            print(f"Kafka User: {datastore.kkuser}")
        if datastore.kksecret:
            print(f"Kafka Secret: {datastore.kksecret}")
        if datastore.kk_sasl_mechanism:
            print(f"Kafka SASL Mechanism: {datastore.kk_sasl_mechanism}")
        if datastore.kk_security_protocol:
            print(f"Kafka Security Protocol: {datastore.kk_security_protocol}")
        if datastore.kk_sasl_jaas_config:
            print(f"Kafka SASL JAAS Config: {datastore.kk_sasl_jaas_config}")
        if datastore.kk_ssl_endpoint_identification_algo:
            print(
                f"Kafka SSL Endpoint ID Algorithm: {datastore.kk_ssl_endpoint_identification_algo}"
            )
        if datastore.kk_ssl_ts_type:
            print(f"Kafka SSL TS Type: {datastore.kk_ssl_ts_type}")
        if datastore.kk_ssl_ts_certificates:
            print(f"Kafka SSL TS Certificates: {datastore.kk_ssl_ts_certificates}")
        if datastore.kk_ssl_ts_location:
            print(f"Kafka SSL TS Location: {datastore.kk_ssl_ts_location}")
        if datastore.kk_ssl_ts_password:
            print(f"Kafka SSL TS Password: {datastore.kk_ssl_ts_password}")
        if datastore.kk_ssl_ks_type:
            print(f"Kafka SSL KS Type: {datastore.kk_ssl_ks_type}")
        if datastore.kk_ssl_ks_location:
            print(f"Kafka SSL KS Location: {datastore.kk_ssl_ks_location}")
        if datastore.kk_ssl_ks_password:
            print(f"Kafka SSL KS Password: {datastore.kk_ssl_ks_password}")
        if datastore.schemaregapikey:
            print(f"Schema Registry API Key: {datastore.schemaregapikey}")
        if datastore.schemaregsecret:
            print(f"Schema Registry Secret: {datastore.schemaregsecret}")

        print("\n\n\n")

        filter_query = f"SELECT * FROM tst1a.users_latest WHERE useremail = '{current_user['sub']}'"
        conn = get_sqlalchemy_conn()
        df = pd.read_sql(filter_query, conn)
        print(df)
        if df.empty:
            return response(404, "Dataset not found.")
        conn.commit()
        return response(200, "Test connection successful!")
    except Exception as e:
        return response(500, f"Test connection failed: {str(e)}")
