from pydantic import BaseModel


class DatastoreBase(BaseModel):
    dsshortname: str
    datastorename: str
    dstype: str
    driver: str | None = None
    url: str | None = None
    username: str | None = None
    passwrd: str | None = None
    tablename: str | None = None


class Datastore(DatastoreBase):
    useremail: str | None = None
    is_valid: bool | None = None
    aws_iam_role: str | None = None
    tempdir: str | None = None
    credentials_file: str | None = None
    createdate: str | None = None
    gcp_projectid: str | None = None
    gcp_datasetid: str | None = None
    gcp_tableid: str | None = None
    sfaccount: str | None = None
    sfdb: str | None = None
    sfschema: str | None = None
    sfwarehouse: str | None = None
    sfRole: str | None = None
    bootstrap_servers: str | None = None
    topic: str | None = None
    schemareg_url: str | None = None
    kkuser: str | None = None
    kksecret: str | None = None
    kk_sasl_mechanism: str | None = None
    kk_security_protocol: str | None = None
    kk_sasl_jaas_config: str | None = None
    kk_ssl_endpoint_identification_algo: str | None = None
    kk_ssl_ts_type: str | None = None
    kk_ssl_ts_certificates: str | None = None
    kk_ssl_ts_location: str | None = None
    kk_ssl_ts_password: str | None = None
    kk_ssl_ks_type: str | None = None
    kk_ssl_ks_location: str | None = None
    kk_ssl_ks_password: str | None = None
    schemaregapikey: str | None = None
    schemaregsecret: str | None = None
    is_target: str | None = None
    bucketname: str | None = None
    subdirectory: str | None = None
