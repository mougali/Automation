DECLARE

	v_stmt_str VARCHAR2(1000) := 'INSERT INTO PLATFORM_STCK VALUES(:g_pID, :g_pDesc, SYSDATE, SYSDATE, NULL)';

	-- Backups for config tables
	v_stmt_create1 VARCHAR2(1000) := 'create table PLATFORM_STCK_BKP_&1 as select * from PLATFORM_STCK';
	v_stmt_create2 VARCHAR2(1000) := 'create table PLATFORM_DTL_BKP_&1 as select * from PLATFORM_DTL';
	v_stmt_create3 VARCHAR2(1000) := 'create table CONNECTION_DETAILS_&1 as select * from CONNECTION_DETAILS';
	v_stmt_create4 VARCHAR2(1000) := 'create table PROP_CNTNT_BKP_&1 as select * from PROP_CNTNT';
	v_stmt_create5 VARCHAR2(1000) := 'create table OPT_TAB_COL_BKP_&1 as select * from OPT_TAB_COL';
	v_stmt_create6 VARCHAR2(1000) := 'create table SRC_BKP_&1 as select * from SRC';
	v_stmt_create7 VARCHAR2(1000) := 'create table CLNT_BKP_&1 as select * from CLNT';

	-- Backups for config tables loaded via seed-files
	v_stmt_create8 VARCHAR2(1000) := 'CREATE TABLE PRCS_CONF_&1 AS SELECT * FROM PRCS_CONF';
	v_stmt_create9 VARCHAR2(1000) := 'CREATE TABLE OBJ_GRP_&1 AS SELECT *  FROM OBJ_GRP';
	v_stmt_create10 VARCHAR2(1000) := 'CREATE TABLE SBJ_AREA_&1 AS SELECT *  FROM SBJ_AREA';
	v_stmt_create11 VARCHAR2(1000) := 'CREATE TABLE OBJ_&1 AS SELECT *  FROM OBJ';
	v_stmt_create12 VARCHAR2(1000) := 'CREATE TABLE DIM_&1 AS SELECT *  FROM DIM';
	v_stmt_create13 VARCHAR2(1000) := 'CREATE TABLE STD_FMT_META_DTA_&1 AS SELECT *  FROM STD_FMT_META_DTA';
	v_stmt_create14 VARCHAR2(1000) := 'CREATE TABLE SRVC_ORCH_&1 AS SELECT *  FROM SRVC_ORCH';
	v_stmt_create15 VARCHAR2(1000) := 'CREATE TABLE OBJ_PRCS_EXCPN_&1 AS SELECT *  FROM OBJ_PRCS_EXCPN';
	v_stmt_create16 VARCHAR2(1000) := 'CREATE TABLE CUST_ADAPT_&1 AS SELECT *  FROM CUST_ADAPT';
	v_stmt_create17 VARCHAR2(1000) := 'CREATE TABLE SUB_DIM_KEY_&1 AS SELECT *  FROM SUB_DIM_KEY';

	var_platformID NUMBER(10, 0) := &16;
	-- var_platformIdProp matches the data definition in the PROP_CNTN table; contains same value as var_platformID
	var_platformIdProp NUMBER(20, 0) := &16;
	var_connectionID NUMBER(10, 0) := &17;
	var_platformDesc VARCHAR2(100 BYTE) := '&3';
	var_srcID NUMBER(20, 0) := &4;
	
	-- Parameters used for SRC table
	var_srcIdSRC NUMBER(10, 0) := &4;		-- Used for SRC table, which has different data definition than PROP_CNTNT
	var_srcCode CHAR(3 BYTE) := '&2';
	var_srcDsc VARCHAR2(100 BYTE) := '&3';
	var_ckaSubID NUMBER(10, 0) := &6;
	var_ckaSubNm VARCHAR2(30 BYTE) := '&5';

	-- Parameters used for CLNT table
	var_clientID NUMBER(10, 0) := &9;
	var_clientCode VARCHAR2(10 BYTE) := '&7';
	var_clientDsc VARCHAR2(30 BYTE) := '&8';


	/* Parameters for CONNECTION_DETAILS table */
	var_ntzServ VARCHAR2 (100 BYTE) := '&10';
	var_ntzUID VARCHAR2 (100 BYTE) := '&11';
	var_ntzDB VARCHAR2 (100 BYTE) := '&12';
	var_ntzPW VARCHAR2 (100 BYTE) := '&13';
	var_ntzOdsDB VARCHAR2 (100 BYTE) := '&14';
	var_ntzCkrDB VARCHAR2 (100 BYTE) := '&15';

BEGIN
	
	/* BEGIN config table backup */
	EXECUTE IMMEDIATE v_stmt_create1;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create2;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create3;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create4;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create5;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create6;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create7;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create8;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create9;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create10;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create11;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create12;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create13;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create14;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create15;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create16;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_create17;
	COMMIT;
	/* END config table backup */

	EXECUTE IMMEDIATE v_stmt_str
		USING var_platformID, var_platformDesc;
	COMMIT;

	/* INSERT new records into PLATFORM_DTL table */
	v_stmt_str := 'INSERT INTO PLATFORM_DTL(PLTFM_ID, CONNECTION_ID) VALUES(:g_pID,1)';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_platformID;
	COMMIT;

	v_stmt_str := 'INSERT INTO PLATFORM_DTL(PLTFM_ID, CONNECTION_ID) VALUES(:g_pID,:g_cID)';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_platformID, var_connectionID;
	COMMIT;

	/* INSERT new records into CONNECTION_DETAILS table */
	v_stmt_str := q'$INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(:g_cID,'NTZ_ODS_STG_SVR',:pVal)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_connectionID, var_ntzServ;
	COMMIT;

	v_stmt_str := q'$INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(:g_cID,'NTZ_ODS_STG_UID',:pVal)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_connectionID, var_ntzUID;
	COMMIT;

	v_stmt_str := q'$INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(:g_cID,'NTZ_ODS_STG_DB',:pVal)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_connectionID, var_ntzDB;
	COMMIT;

	v_stmt_str := q'$INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(:g_cID,'NTZ_ODS_STG_PW',:pVal)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_connectionID, var_ntzPW;
	COMMIT;

	v_stmt_str := q'$INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(:g_cID,'NTZ_ODS_ODS_DB',:pVal)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_connectionID, var_ntzOdsDB;
	COMMIT;

	v_stmt_str := q'$INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(:g_cID,'NTZ_ODS_CKR_DB',:pVal)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_connectionID, var_ntzCkrDB;
	COMMIT;


	/*************************************** INSERT into PROP_CNTNT table ******************************************************
	*******************************************************************************************************************************************
	*******************************************************************************************************************************************/
	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#!/bin/sh',1)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,2)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Netezza Tlog Staging Database',3)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_STG_HOST="${NTZ_ODS_STG_SVR}"',4)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_STG_DB="${NTZ_ODS_STG_DB}"',5)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_STG_USER="${NTZ_ODS_STG_UID}"',6)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_STG_PASS="${NTZ_ODS_STG_PW}"',7)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,8)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Netezza Tlog Staging Database',9)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_ODS_HOST="${NTZ_ODS_STG_SVR}"',10)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_ODS_DB="${NTZ_ODS_ODS_DB}"',11)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_ODS_USER="${NTZ_ODS_STG_UID}"',12)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_ODS_PASS="${NTZ_ODS_STG_PW}"',13)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,14)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Netezza Tlog Staging Database',15)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_CKR_HOST="${NTZ_ODS_STG_SVR}"',16)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_CKR_DB="${NTZ_ODS_CKR_DB}"',17)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_CKR_USER="${NTZ_ODS_STG_UID}"',18)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_CKR_PASS="${NTZ_ODS_STG_PW}"',19)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,20)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Oracle ABC Database',21)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export ABC_UNM=${ORA_CMI_ABC_SCHEMA}',22)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export ABC_PWD=${ORA_CMI_ABC_PW}',23)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export ABC_DBNM=${ORA_CMI_DB}',24)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export ABC_DB_NM=${ORA_CMI_ABC_SCHEMA}',25)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,26)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Oracle Configuration Database',27)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CFG_DB_USR=${ORA_CMI_CONFIG_SCHEMA}',28)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CFG_DB_PWD=${ORA_CMI_CONFIG_PW}',29)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CFG_DB_SRVR=${ORA_CMI_DB}',30)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CFG_DB_NM=${ORA_CMI_CONFIG_SCHEMA}',31)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,32)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#DIMENSION LIST FOR PULL NATURAL KEYS',33)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',q'!export DIMENSION_LIST="'PRODUCT','PERIOD','STORE','BASKET','HOUSEHOLD','PERSON','IDENTIFYING_CARD','LANE'"!',34)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,35)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Application Specific',36)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export REQUESTER_NAME=TLOGAPP',37)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,38)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export FL_WTCH_RTRN_CD=99',39)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CHK_TOT_FLS_RTRN_CD=199',40)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,41)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Source tables',42)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export ABC_HIGH_LOW=ABC_HIGH_LOW',43)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,44)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#ABC Tables',45)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export ODABC_DB=${ABC_UNM}',46)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export BATCH_TRCK=${ODABC_DB}.BATCH_TRCK',47)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export FL_RGSTR_TBL=${ODABC_DB}.FL_RGSTR',48)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,49)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Configuration Tables',50)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CONFIG_DB=${CFG_DB_USR}',51)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export SBJ_AREA_TBL=${CONFIG_DB}.SBJ_AREA',52)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export SRC=${CONFIG_DB}.SRC',53)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export DIM=${CONFIG_DB}.DIM',54)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CUST_ADAPT_TBL=${CONFIG_DB}.CUST_ADAPT',55)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export OBJ_GRP_TBL=${CONFIG_DB}.OBJ_GRP',56)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#########CKA IDLE TIME',57)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,58)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CKA_Resv_IdleTm=15 seconds',59)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CKA_Resv_IdleLimit=6',60)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,61)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Directory paths',62)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export APPHOME=$APP_HOME',63)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CODEDIR=${APPHOME}/code',64)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export BINDIR=${CODEDIR}/bin',65)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CUST_ADPTR_BINDIR=${BINDIR}/cust_adapter',66)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TRIP_CUST_ADPTR_BINDIR=${BINDIR}/trip_cust_adapter',67)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export PROPDIR=${CODEDIR}/properties',68)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export ORASQL=${CODEDIR}/sql',69)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export LOGDIR=${APPHOME}/logs',70)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export WRKDIR=${APPHOME}/working',71)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export SQLDIR=${WRKDIR}/sql',72)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TEMPDIR=${WRKDIR}/tmp',73)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export COMMON_DIR=${APPHOME}/code/bin',74)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export DATADIR=${APPHOME}/data',75)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export OUTPUTDIR=${DATADIR}/outputs',76)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export INPUTDIR=${DATADIR}/inputs',77)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export STGDIR=${OUTPUTDIR}/staging',78)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export LOADDIR=${OUTPUTDIR}/loading',79)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CONFIG_DATA=${INPUTDIR}/config',80)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export INITLOAD_DIR=${INPUTDIR}/init_load',81)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export LANDING_DIR=${INPUTDIR}/landing',82)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,83)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#CKA Meta and Data file Directories',84)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CKA_APPHOME=${DSG_CKA_APP_PATH}',85)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CKA_BIN=${CKA_APPHOME}/code/bin',86)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export DATAOUT_DIR=${CKA_APPHOME}/data/inputs/xml',87)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export DATAIN_DIR=${CKA_APPHOME}/data/outputs/xml',88)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,89)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Local Meta and Data file Directories',90)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export DATAINLOCAL_DIR=${INPUTDIR}/xml',91)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export DATAOUTLOCAL_DIR=${OUTPUTDIR}/xml',92)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,93)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export DATAINARCH_DIR=${XMLINLOCAL_DIR}/archive',94)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export DATAOUTARCH_DIR=${XMLOUTLOCAL_DIR}/archive',95)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export DATAOUT_REJ_DIR=${XMLOUTLOCAL_DIR}/rejects',96)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export DATAIN_REJ_DIR=${XMLINLOCAL_DIR}/rejects',97)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,98)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Local XML Directories',99)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export XMLINLOCAL_DIR=${INPUTDIR}/xml',100)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export XMLOUTLOCAL_DIR=${OUTPUTDIR}/xml',101)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,102)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export XMLINARCH_DIR=${XMLINLOCAL_DIR}/archive',103)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export XMLOUTARCH_DIR=${XMLOUTLOCAL_DIR}/archive',104)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export XMLOUT_REJ_DIR=${XMLOUTLOCAL_DIR}/rejects',105)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export XMLIN_REJ_DIR=${XMLINLOCAL_DIR}/rejects',106)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,107)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#CKA XML Directories',108)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CKA_APPHOME=${DSG_CKA_APP_PATH}',109)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CKA_BIN=${CKA_APPHOME}/code/bin',110)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export XMLOUT_DIR=${CKA_APPHOME}/data/inputs/xml',111)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export XMLIN_DIR=${CKA_APPHOME}/data/outputs/xml',112)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,113)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Common Process',114)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CMMN_PRCS_FUNCDIR=${REL_HOME}/common_processes/code/functions',115)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CMMN_PRCS_PROPDIR=${REL_HOME}/common_processes/code/properties',116)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,117)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Dim Sourcing TEMP*****************',118)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','##export DSMNTR_HOME=${REL_HOME}/dimension_sourcing',119)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,120)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Keying Properties',121)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export ARCHV_DAYS=7',122)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,123)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#DSjob directory',124)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_DSPROJNAME=${DSG_TLOG_PROJ}',125)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,126)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Misc properties',127)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#xport MAIL_RECIPIENT="udhayapriya.maruthaiyan.ap@nielsen.com"',128)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#export MAIL_RECIPIENT="jayasubha.kanakaraj.ap@nielsen.com"',129)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export MAIL_RECIPIENT=""',130)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,131)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#ODS Properties',132)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export ODS_SQL_CONFIG=${PROPDIR}/ods_sql_properties.conf',133)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export LOAD_PARSER=${BINDIR}/tlog_parse_sqlconf.awk',134)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export TLOG_HISTORY=LOAD_HIST',135)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export VAL_PARSER=${BINDIR}/tlog_parse_val.awk',136)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export ODS_BKP_TRSHLD=7',137)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export WEEKLY_BKP_DAY=3,4,5',138)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export WBKP_THRESHOLD=7',139)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,140)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Combine Data Restatement Properties',141)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export RESTMT_AREA_BAS="BAR"',142)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export RESTMT_AREA_ITM="ITR"',143)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export RESTMT_AREA_BNI="BNR"',144)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export RESTMT_AREA_BDI="BRS"',145)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export RESTMT_AREA_BID="BIR"',146)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#export RESTMT_AREA_AGP="AGR"',147)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export RESTMT_AREA_AGP="RGP"',148)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export RESTMT_AREA_HHA="HAR"',149)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export RESTMT_AREA_HHS="HHR"',150)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,151)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,152)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#######################################################',153)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','# Variables added temporarily for IDC Keying workaround',154)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','# To be removed once workaround is no longer needed',155)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#######################################################',156)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#Oracle CKA Database',157)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CKA_UNM=${ORA_CKAADV_CKAADV_SCHEMA}',158)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CKA_PWD=${ORA_CKAADV_CKAADV_PW}',159)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CKA_DBNM=${ORA_CKAADV_DB}',160)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CKA_DB_NM=${ORA_CKAADV_CKAADV_SCHEMA}',161)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,162)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,163)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','########################################',164)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','# Variables for Historical Load Wrapper',165)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','########################################',166)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export BATCH_THRSHLD=5',167)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export MANIFEST_WAIT=600',168)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export BATCH_WAIT=600',169)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,170)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','########################################',171)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','# Process Event Servirities',172)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','########################################',173)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export SC_DEBUG="-1"',174)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export SC_INFO="0"',175)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export SC_WARNING="1"',176)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export SC_ERROR="2"',177)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export SC_FATAL="FATAL"',178)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,179)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,180)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#######################################',181)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#SAS Extract Variables',182)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#######################################',183)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export SAS_EXTRACT_OUTPUT_DIR=/ido/od251dev/data/nsk',184)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export EMAIL_IDS="Robert.Moore.ap@nielsen.com;Varaprasad.Kadali.ap@nielsen.com"',185)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	----------------------------Change the email id to Laxmi or ODS group id---------------------

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export RMT_ENV_ID="301"',186)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,187)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#######################################',188)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#2.9 Changes',189)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#######################################',190)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export GRP_COMPLTNESS_DATLMT=2',191)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export CHK_TOT_DAYLMT=10',192)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,193)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','####################################3',194)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','#nzload changes',195)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','####################################',196)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export MAX_ERR=1',197)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh',null,198)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','####################################',199)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','# FILE WATCHER VARIABLES',200)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','####################################',201)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	v_stmt_str := q'$Insert into PROP_CNTNT (SOURCE_ID,PLATFORM_ID,PROP_FL_NM,PROP_FL_CNTNT,LINE_NUM) values (:g_srcID,:g_pID,'LOYALTY_tlog_properties.ksh','export FL_STBLIZE_CNT=3',202)$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcID, var_platformIdProp;
	COMMIT;

	/********************************* INSERT INTO SOURCE AND CLIENT TABLES ***************************************/
	--SRC and CLNT for Casino
	v_stmt_str := q'$INSERT INTO SRC (SRC_ID,SRC_CD,SRC_DSC,CKA_SUB_ID,CKA_SUB_NM,CRT_DT,LST_UPD_DT,LST_UPD_USR,SRC_STS) VALUES (:g_srcID,:g_srcCd,:g_srcDsc,:g_ckaID,:g_ckaNm,SYSDATE,SYSDATE,'LCRODCONFIGQ','I')$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_srcIdSRC, var_srcCode, var_srcDsc, var_ckaSubID, var_ckaSubNm;
	COMMIT;

	v_stmt_str := q'$INSERT INTO CLNT (CLNT_ID,CLNT_CD,CLNT_DSC,CRT_DT,LST_UPD_DT,LST_UPD_USR) VALUES (seq_clnt_id.NEXTVAL,:g_clntCode,:g_clntDsc,SYSDATE,SYSDATE,'LCRODCONFIGQ')$';
	EXECUTE IMMEDIATE v_stmt_str
		USING var_clientCode, var_clientDsc;
	COMMIT;

END;
/