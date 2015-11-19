CREATE OR REPLACE PROCEDURE
Create_Tables
IS
BEGIN
	create table PLATFORM_STCK_BKP_&1 as select * from PLATFORM_STCK;
	create table PLATFORM_DTL_BKP_&1 as select * from PLATFORM_DTL;
	create table CONNECTION_DETAILS_&1 as select * from CONNECTION_DETAILS;
	create table PROP_CNTNT_BKP_&1 as select * from PROP_CNTNT;
	create table OPT_TAB_COL_BKP_&1 as select * from OPT_TAB_COL;
	create table SRC_BKP_&1 as select * from SRC ;
	create table CLNT_BKP_&1 as select * from CLNT;

	DBMS_OUTPUT.put_line (SQL%ROWCOUNT);
END;

CREATE OR REPLACE PROCEDURE
Insert_Platform_Stack
IS
DECLARE
	var_platformID NUMBER(10, 0) := &16
	var_platformDesc VARCHAR2(100 BYTE) := "New platform for Wal-Mart"
BEGIN
	INSERT INTO PLATFORM_STCK VALUES(var_platformID, var_platformDesc, SYSDATE, SYSDATE, NULL);

	DBMS_OUTPUT.put_line (SQL%ROWCOUNT);
END;

/*
CREATE OR REPLACE PROCEDURE
Insert_Platform_Detail
BEGIN
	INSERT INTO PLATFORM_DTL(PLTFM_ID, CONNECTION_ID) VALUES(&16,1);
	INSERT INTO PLATFORM_DTL(PLTFM_ID, CONNECTION_ID) VALUES(&16,&17);

	DBMS_OUTPUT.put_line (SQL%ROWCOUNT);
END;

CREATE OR REPLACE PROCEDURE
Insert_Connection_Detail
BEGIN
	INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(&17,'NTZ_ODS_STG_SVR','&10');
	INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(&17,'NTZ_ODS_STG_UID','&11');
	INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(&17,'NTZ_ODS_STG_DB','&12');
	INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(&17,'NTZ_ODS_STG_PW','&13');
	INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(&17,'NTZ_ODS_ODS_DB','&14');
	INSERT INTO CONNECTION_DETAILS(CONNECTION_ID, PARAMETER_NAME, PARAMETER_VALUE) VALUES(&17,'NTZ_ODS_CKR_DB','&15');

	DBMS_OUTPUT.put_line (SQL%ROWCOUNT);
END;
*/


BEGIN
	Create_Tables;
	Insert_Platform_Stack;
	COMMIT;
END;
/