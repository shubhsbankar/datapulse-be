-- -- Add this at the beginning of the file
-- \c tst1a;

-- CREATE SCHEMA IF NOT EXISTS tst1a;

-- CREATE SEQUENCE IF NOT EXISTS tst1a.rdvcomp_rdvid_seq;

-- CREATE TABLE IF NOT EXISTS tst1a.projects
-- (
--     projectid serial,
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     projectname character varying(60) COLLATE pg_catalog."default",
--     coname character varying(30) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     user_email character varying(100) COLLATE pg_catalog."default",
--     CONSTRAINT projects_pkey PRIMARY KEY (projectshortname)
-- );

-- CREATE TABLE IF NOT EXISTS tst1a.projectassignments_latest
-- (
--     assignid serial,
--     useremail character varying(70) COLLATE pg_catalog."default" NOT NULL,
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     is_active boolean DEFAULT true,
--     who_added character varying(50) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT assign_pkey1 PRIMARY KEY (useremail, projectshortname)
-- );

-- CREATE TABLE IF NOT EXISTS tst1a.projectassignments_append
-- (
--     assignid serial,
--     useremail character varying(70) COLLATE pg_catalog."default" NOT NULL,
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     is_active boolean DEFAULT true,
--     who_added character varying(50) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT assign_pkey2 PRIMARY KEY (assignid)
-- );

-- CREATE OR REPLACE VIEW tst1a.vw_projectassignments_latest AS
--  SELECT pal.assignid,
--     pal.useremail,
--     pa.projectname,
--     pal.is_active,
--     pal.who_added,
--     pal.createdate    
--    FROM tst1a.projectassignments_latest pal
--      JOIN tst1a.projects pa ON pal.projectshortname = pa.projectshortname;

-- CREATE OR REPLACE VIEW tst1a.vw_projectassignments_append AS
--  SELECT paa.assignid,
--     paa.useremail,
--     pa.projectname,
--     paa.is_active,
--     paa.who_added,
--     paa.createdate    
--    FROM tst1a.projectassignments_append paa
--      JOIN tst1a.projects pa ON paa.projectshortname = pa.projectshortname;



-- CREATE TABLE IF NOT EXISTS tst1a.users_latest
-- (
--     userid serial,
--     useremail character varying(70) COLLATE pg_catalog."default" NOT NULL UNIQUE,
--     password character varying(80) COLLATE pg_catalog."default",
--     first_name character varying(50) COLLATE pg_catalog."default",
--     last_name character varying(50) COLLATE pg_catalog."default",
--     user_type character varying(20) COLLATE pg_catalog."default" DEFAULT 'user',
--     who_added character varying(50) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT users_pkey1 PRIMARY KEY (useremail)
-- );

-- CREATE TABLE IF NOT EXISTS tst1a.users_append
-- (
--     userid serial,
--     useremail character varying(70) COLLATE pg_catalog."default",
--     password character varying(80) COLLATE pg_catalog."default",
--     first_name character varying(50) COLLATE pg_catalog."default",
--     last_name character varying(50) COLLATE pg_catalog."default",
--     user_type character varying(20) COLLATE pg_catalog."default",
--     who_added character varying(50) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT users_pkey2 PRIMARY KEY (userid)
-- );

-- CREATE TABLE IF NOT EXISTS tst1a.datastores
-- (
--     dsid serial,
--     dsshortname character varying(30) COLLATE pg_catalog."default" NOT NULL,
--     datastorename character varying(40) COLLATE pg_catalog."default",
--     dstype character varying(40) COLLATE pg_catalog."default",
--     url character varying(120) COLLATE pg_catalog."default",
--     driver character varying(100) COLLATE pg_catalog."default",
--     username character varying(50) COLLATE pg_catalog."default",
--     passwrd character varying(50) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     tablename character varying(50) COLLATE pg_catalog."default",
--     useremail character varying(50) COLLATE pg_catalog."default" NOT NULL,
--     is_valid boolean DEFAULT false,
--     aws_iam_role character varying(100) COLLATE pg_catalog."default",
--     tempdir character varying(100) COLLATE pg_catalog."default",
--     credentials_file character varying(120) COLLATE pg_catalog."default",
--     gcp_projectid character varying(60) COLLATE pg_catalog."default",
--     gcp_datasetid character varying(60) COLLATE pg_catalog."default",
--     gcp_tableid character varying(60) COLLATE pg_catalog."default",
--     sfaccount character varying(60) COLLATE pg_catalog."default",
--     sfdb character varying(60) COLLATE pg_catalog."default",
--     sfschema character varying(60) COLLATE pg_catalog."default",
--     sfwarehouse character varying(60) COLLATE pg_catalog."default",
--     sfRole character varying(60) COLLATE pg_catalog."default",
--     bootstrap_servers character varying(200) COLLATE pg_catalog."default",
--     topic character varying(50) COLLATE pg_catalog."default",
--     schemareg_url character varying(120) COLLATE pg_catalog."default",
--     kkuser character varying(50) COLLATE pg_catalog."default",
--     kksecret character varying(50) COLLATE pg_catalog."default",
--     kk_sasl_mechanism character varying(50) COLLATE pg_catalog."default",
--     kk_security_protocol character varying(50) COLLATE pg_catalog."default",
--     kk_sasl_jaas_config character varying(250) COLLATE pg_catalog."default",
--     kk_ssl_endpoint_identification_algo character varying(50) COLLATE pg_catalog."default",
--     kk_ssl_ts_type character varying(30) COLLATE pg_catalog."default",
--     kk_ssl_ts_certificates character varying(100) COLLATE pg_catalog."default",
--     kk_ssl_ts_location character varying(100) COLLATE pg_catalog."default",
--     kk_ssl_ts_password character varying(50) COLLATE pg_catalog."default",
--     kk_ssl_ks_type character varying(30) COLLATE pg_catalog."default",
--     kk_ssl_ks_location character varying(100) COLLATE pg_catalog."default",
--     kk_ssl_ks_password character varying(50) COLLATE pg_catalog."default",
--     schemaregapikey character varying(50) COLLATE pg_catalog."default",
--     schemaregsecret character varying(50) COLLATE pg_catalog."default",
--     CONSTRAINT datastores_pkey PRIMARY KEY (dsshortname)
-- );

-- -- Dummy data

-- INSERT INTO tst1a.users_latest (useremail, password, first_name, last_name, user_type, who_added) VALUES ('admin@office1.com', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin', 'admin', 'admin', 'admin');













-- -- USER ddl


-- CREATE TABLE IF NOT EXISTS tst1a.datasets
-- (
--     datasetid serial,
--     datasettype character varying(10) COLLATE pg_catalog."default",
--     csvname character varying(50) COLLATE pg_catalog."default",
--     tablename character varying(60) COLLATE pg_catalog."default",
--     csvdailysuffix character varying(5) COLLATE pg_catalog."default",
--     datasetshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     datastoreshortname character varying(30) COLLATE pg_catalog."default" NOT NULL,
--     dataproductshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     domainshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     separator character varying(5) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     dsdatatype character varying(10) COLLATE pg_catalog."default" NOT NULL,
--     --fieldtype character varying(12) COLLATE pg_catalog."default",
--     fieldname character varying(30) COLLATE pg_catalog."default",
--     is_valid character varying(5) COLLATE pg_catalog."default",
--     useremailid character varying(50) COLLATE pg_catalog."default",
--     sourcename character varying(30) COLLATE pg_catalog."default",
--     tenantid character varying(30) COLLATE pg_catalog."default",
--     bkcarea character varying(30) COLLATE pg_catalog."default",
--     filessource character varying(20) COLLATE pg_catalog."default",
--     filesbucketpath character varying(100) COLLATE pg_catalog."default",
--     s3_accesskey character varying(100) COLLATE pg_catalog."default",
--     s3_secretkey character varying(100) COLLATE pg_catalog."default",
--     gcs_jsonfile character varying(100) COLLATE pg_catalog."default",
--     CONSTRAINT datasets_pkey PRIMARY KEY (projectshortname, datasetshortname, dataproductshortname)
-- );

-- CREATE TABLE IF NOT EXISTS tst1a.dping
-- (
--     dpid serial,
--     dpshortname character varying(120) COLLATE pg_catalog."default" NOT NULL,
--     htmlfilename character varying(120) COLLATE pg_catalog."default",
--     datasettype character varying(20) COLLATE pg_catalog."default",
--     projectshortname character varying(40) COLLATE pg_catalog."default",
--     datasetshortname character varying(40) COLLATE pg_catalog."default",
--     dataproductshortname character varying(40) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     useremailid character varying(70) COLLATE pg_catalog."default",
--     CONSTRAINT dping_pkey PRIMARY KEY (dpshortname)
-- );

-- CREATE TABLE IF NOT EXISTS tst1a.dtg
-- (
--     dtid serial,
--     dtshortname character varying(120) COLLATE pg_catalog."default" NOT NULL,
--     chkfilename character varying(120) COLLATE pg_catalog."default",
--     datasettype character varying(20) COLLATE pg_catalog."default",
--     datasrcnum character varying(3) COLLATE pg_catalog."default",
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     datasetshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     dataproductshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     useremailid character varying(70) COLLATE pg_catalog."default",
--     testcoverageversion character varying(10) COLLATE pg_catalog."default",
--     comments character varying(250) COLLATE pg_catalog."default",
--     CONSTRAINT dtg_pkey PRIMARY KEY (projectshortname, dtshortname, dataproductshortname, datasetshortname)
-- );

-- CREATE TABLE IF NOT EXISTS tst1a.rs
-- (
--     srchashid serial,
--     projectshortname character varying(40) COLLATE pg_catalog."default",
--     srcdphash character varying(150) COLLATE pg_catalog."default",
--     srcdataset character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     srctabfields text[] COLLATE pg_catalog."default",
--     tablename character varying(60) COLLATE pg_catalog."default",
--     datastoreshortname character varying(40) COLLATE pg_catalog."default",
--     srchashcol character varying(100) COLLATE pg_catalog."default",
--     dpname character varying(50) COLLATE pg_catalog."default" NOT NULL,
--     bkeys character varying(5) COLLATE pg_catalog."default",
--     bkey1 character varying(40) COLLATE pg_catalog."default",
--     bkey2 character varying(40) COLLATE pg_catalog."default",
--     bkey3 character varying(40) COLLATE pg_catalog."default",
--     bkey4 character varying(40) COLLATE pg_catalog."default",
--     bkey5 character varying(40) COLLATE pg_catalog."default",
--     bkey6 character varying(40) COLLATE pg_catalog."default",
--     bkey7 character varying(40) COLLATE pg_catalog."default",
--     bkey8 character varying(40) COLLATE pg_catalog."default",
--     bkey9 character varying(40) COLLATE pg_catalog."default",
--     bkey10 character varying(40) COLLATE pg_catalog."default",
--     useremailid character varying(70) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT rs_pkey PRIMARY KEY (projectshortname, dpname, srcdataset)
-- );

-- CREATE TABLE IF NOT EXISTS tst1a.rt
-- (
--     tgthashid serial,
--     projectshortname character varying(40) COLLATE pg_catalog."default",
--     tgtdphash character varying(150) COLLATE pg_catalog."default",
--     tgtdataset character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     tgttabfields text[] COLLATE pg_catalog."default",
--     tgthashcol character varying(100) COLLATE pg_catalog."default",
--     dpname character varying(50) COLLATE pg_catalog."default" NOT NULL,
--     tablename character varying(60) COLLATE pg_catalog."default",
--     datastoreshortname character varying(40) COLLATE pg_catalog."default",
--     bkeys character varying(5) COLLATE pg_catalog."default",
--     bkey1 character varying(40) COLLATE pg_catalog."default",
--     bkey2 character varying(40) COLLATE pg_catalog."default",
--     bkey3 character varying(40) COLLATE pg_catalog."default",
--     bkey4 character varying(40) COLLATE pg_catalog."default",
--     bkey5 character varying(40) COLLATE pg_catalog."default",
--     bkey6 character varying(40) COLLATE pg_catalog."default",
--     bkey7 character varying(40) COLLATE pg_catalog."default",
--     bkey8 character varying(40) COLLATE pg_catalog."default",
--     bkey9 character varying(40) COLLATE pg_catalog."default",
--     bkey10 character varying(40) COLLATE pg_catalog."default",
--     useremailid character varying(70) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT rt_pkey PRIMARY KEY (projectshortname, dpname, tgtdataset)
-- );


-- CREATE TABLE IF NOT EXISTS tst1a.str
-- (
--     srctgthashid serial,
--     projectshortname character varying(40) COLLATE pg_catalog."default",
--     srctgthash character varying(300) COLLATE pg_catalog."default" NOT NULL,
--     srchash character varying(150) COLLATE pg_catalog."default",
--     tgthash character varying(150) COLLATE pg_catalog."default",
--     rtype character varying(40) COLLATE pg_catalog."default",
--     rdata character varying(40) COLLATE pg_catalog."default",
--     rfield character varying(40) COLLATE pg_catalog."default",
--     hr_exec character varying(2) COLLATE pg_catalog."default",
--     useremailid character varying(70) COLLATE pg_catalog."default",
--     rsbkeys character varying(5) COLLATE pg_catalog."default",
--     rtbkeys character varying(5) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT srctgthash_pkey PRIMARY KEY (projectshortname, srctgthash)
-- );

-- CREATE TABLE IF NOT EXISTS tst1a.tenantbkcc
-- (
--     tenantid character varying(50) COLLATE pg_catalog."default" NOT NULL,
--     bkcarea character varying(50) COLLATE pg_catalog."default" NOT NULL,
--     hubname character varying(50) COLLATE pg_catalog."default" NOT NULL,
--     bkcc character varying(40) COLLATE pg_catalog."default",
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     user_email character varying(100) COLLATE pg_catalog."default",
--     CONSTRAINT tenantbkcc_pkey PRIMARY KEY (tenantid, bkcarea, hubname)
-- );

-- -- add one record with 'default'  value for tenantid, bkcarea and hubname

-- CREATE TABLE IF NOT EXISTS tst1a.rdvcompdh
-- (
--     rdvid integer NOT NULL DEFAULT nextval('tst1a.rdvcomp_rdvid_seq'::regclass),
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     dpname character varying(150) COLLATE pg_catalog."default",
--     dsname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     comptype character varying(14) COLLATE pg_catalog."default",
--     compname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     compkeyname character varying(50) COLLATE pg_catalog."default" NOT NULL, 
--     bkfields text[] COLLATE pg_catalog."default" NOT NULL,
--     tenantid character varying(50) COLLATE pg_catalog."default",
--     bkcarea character varying(50) COLLATE pg_catalog."default",    
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- --  compshortname is the concat of projectshortname, dpname, dsname, compname, version
--     compshortname character varying(255) COLLATE pg_catalog."default",
--     user_email character varying(100) COLLATE pg_catalog."default",
--     version numeric (5, 2),
--     CONSTRAINT rdvcompdh_pkey PRIMARY KEY (projectshortname, dpname, dsname, compname, version)
-- );



-- CREATE TABLE IF NOT EXISTS tst1a.rdvcompds
-- (
--     rdvid integer NOT NULL DEFAULT nextval('tst1a.rdvcomp_rdvid_seq'::regclass),
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     dpname character varying(150) COLLATE pg_catalog."default",
--     dsname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     comptype character varying(14) COLLATE pg_catalog."default",
--     satlname character varying(50) COLLATE pg_catalog."default" NOT NULL,
--     satlattr text[] COLLATE pg_catalog."default" NOT NULL,
--     assoccomptype character varying(14) COLLATE pg_catalog."default" NOT NULL,
--     assoccompname character varying(40) COLLATE pg_catalog."default" NOT NULL, 
--     tenantid character varying(50) COLLATE pg_catalog."default",
--     bkcarea character varying(50) COLLATE pg_catalog."default",    
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     user_email character varying(100) COLLATE pg_catalog."default",   
-- -- >>compshortname is the concat of projectshortname, dpname, dsname, satlname, version
--     compshortname character varying(255) COLLATE pg_catalog."default",
--     version numeric (5, 2),
--     CONSTRAINT rdvcompds_pkey PRIMARY KEY (projectshortname, dpname, dsname, satlname, version)
-- );


-- CREATE TABLE IF NOT EXISTS tst1a.rdvcompdl
-- (
--     rdvid serial,
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     dpname character varying(150) COLLATE pg_catalog."default",
--     dsname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     comptype character varying(14) COLLATE pg_catalog."default",
--     compname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     compkeyname character varying(50) COLLATE pg_catalog."default" NOT NULL,
--     hubnums integer,
--     hubnum integer,
--     hubname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     hubversion numeric (5, 2), 
--     bkfields text[] COLLATE pg_catalog."default",
--     degen character varying(5) COLLATE pg_catalog."default",    
--     degenids text[] COLLATE pg_catalog."default",
--     tenantid character varying(50) COLLATE pg_catalog."default" NOT NULL,
--     bkcarea character varying(50) COLLATE pg_catalog."default" NOT NULL,    
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     user_email character varying(100) COLLATE pg_catalog."default",   
-- -- >> compshortname is the concat of projectshortname, dpname, dsname, compname, version
--     compshortname character varying(255) COLLATE pg_catalog."default",
--     version numeric (5, 2),
--     CONSTRAINT rdvcompdl_pkey PRIMARY KEY (projectshortname, dpname, dsname, compname, hubname, version)
-- );


-- CREATE TABLE IF NOT EXISTS tst1a.rdvbojds
-- (
--     rdvid serial,
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     dpname character varying(50) COLLATE pg_catalog."default",
--     dsname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     comptype character varying(14) COLLATE pg_catalog."default",
--     compname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     --subtype character varying(30) COLLATE pg_catalog."default" NOT NULL,
--     satlnums integer,
--     satlnum integer,
--     satlname character varying(50) COLLATE pg_catalog."default" NOT NULL, 
--     satlversion numeric (5, 2),
--     tenantid character varying(50) COLLATE pg_catalog."default" NOT NULL,
--     bkcarea character varying(50) COLLATE pg_catalog."default" NOT NULL,    
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- -- >> compshortname is the concat of projectshortname, dpname, dsname, comptype, compname, version
--     compshortname character varying(255) COLLATE pg_catalog."default",
--     user_email character varying(100) COLLATE pg_catalog."default",
--     comments character varying(255) COLLATE pg_catalog."default",
--     version numeric (5, 2),
--     CONSTRAINT rdvbojds_pkey PRIMARY KEY (projectshortname, dpname, dsname, comptype, compname, version, satlname)
-- );



-- CREATE TABLE IF NOT EXISTS tst1a.dvcompsg1
-- (
--     rdvid serial,
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     dpname character varying(50) COLLATE pg_catalog."default",
--     dsname character varying(40) COLLATE pg_catalog."default",
--     comptype character varying(14) COLLATE pg_catalog."default" NOT NULL,
--     compname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     compsubtype character varying(30) COLLATE pg_catalog."default" NOT NULL,
--     sqltext text[] COLLATE pg_catalog."default",
--     tenantid character varying(50) COLLATE pg_catalog."default",
--     bkcarea character varying(50) COLLATE pg_catalog."default",    
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- -- >> compshortname is the concat of projectshortname, comptype, compname
--     compshortname character varying(255) COLLATE pg_catalog."default",
--     user_email character varying(100) COLLATE pg_catalog."default",
--     comments character varying(255) COLLATE pg_catalog."default",
--     version numeric (5, 2),
--     processtype character varying(50) COLLATE pg_catalog."default",
--     datefieldname character varying(50) COLLATE pg_catalog."default",  
--     CONSTRAINT dvcompsg1_pkey PRIMARY KEY (projectshortname, comptype, compname)
-- );



-- CREATE TABLE IF NOT EXISTS tst1a.dvbojsg1
-- (
--     rdvid serial,
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     dpname character varying(50) COLLATE pg_catalog."default",
--     dsname character varying(40) COLLATE pg_catalog."default",
--     comptype character varying(14) COLLATE pg_catalog."default" NOT NULL,
--     compname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     compsubtype character varying(30) COLLATE pg_catalog."default" NOT NULL,
--     sqltext text[] COLLATE pg_catalog."default",
--     tenantid character varying(50) COLLATE pg_catalog."default",
--     bkcarea character varying(50) COLLATE pg_catalog."default",    
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- -- >> compshortname is the concat of projectshortname, comptype, compname, version
--     compshortname character varying(255) COLLATE pg_catalog."default",
--     user_email character varying(100) COLLATE pg_catalog."default",
--     comments character varying(255) COLLATE pg_catalog."default",
--     version numeric (5, 2),
--     processtype character varying(50) COLLATE pg_catalog."default",
--     datefieldname character varying(50) COLLATE pg_catalog."default",  
--     CONSTRAINT dvbojsg1_pkey PRIMARY KEY (projectshortname, comptype, compname, version)
-- );


-- -- New requirements
-- ALTER TABLE tst1a.datastores add is_target character varying(5) COLLATE pg_catalog."default";
-- ALTER TABLE tst1a.datastores add bucketname character varying(100) COLLATE pg_catalog."default";
-- ALTER TABLE tst1a.datastores add subdirectory character varying(100) COLLATE pg_catalog."default";


-- ALTER TABLE tst1a.rdvcompds add partsnum character varying(2) COLLATE pg_catalog."default";
-- ALTER TABLE tst1a.rdvcompds add parts text[] COLLATE pg_catalog."default";

-- ALTER TABLE tst1a.dvcompsg1 add partsnum character varying(2) COLLATE pg_catalog."default";
-- ALTER TABLE tst1a.dvcompsg1 add parts text[] COLLATE pg_catalog."default";

-- ALTER TABLE tst1a.dvbojsg1 add partsnum character varying(2) COLLATE pg_catalog."default";
-- ALTER TABLE tst1a.dvbojsg1 add parts text[] COLLATE pg_catalog."default";

-- ALTER TABLE tst1a.projects add datastoreshortname character varying(40) COLLATE pg_catalog."default";

-- alter table tst1a.datastores add groupname character varying(50) COLLATE pg_catalog."default";

-- CREATE TABLE IF NOT EXISTS tst1a.dvcompsg1b
-- (
--     rdvid serial,
--     projectshortname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     --dpname character varying(50) COLLATE pg_catalog."default",
--     --dsname character varying(40) COLLATE pg_catalog."default",
--     comptype character varying(14) COLLATE pg_catalog."default" NOT NULL,
--     compname character varying(40) COLLATE pg_catalog."default" NOT NULL,
--     compsubtype character varying(30) COLLATE pg_catalog."default" NOT NULL,
--     sqltext text COLLATE pg_catalog."default",
--     --tenantid character varying(50) COLLATE pg_catalog."default",
--     --bkcarea character varying(50) COLLATE pg_catalog."default",    
--     createdate timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     compshortname character varying(255) COLLATE pg_catalog."default",
--     user_email character varying(100) COLLATE pg_catalog."default",
--     comments character varying(255) COLLATE pg_catalog."default",
--     --version numeric (5, 2),
--     --processtype character varying(50) COLLATE pg_catalog."default",
--     --datefieldname character varying(50) COLLATE pg_catalog."default",  
--     CONSTRAINT dvcompsg1b_pkey PRIMARY KEY (projectshortname, comptype, compname)
-- )


-- ALTER TABLE tst1a.users_latest ADD COLUMN is_active BOOLEAN DEFAULT FALSE;
-- ALTER TABLE tst1a.users_append ADD COLUMN is_active BOOLEAN DEFAULT FALSE;