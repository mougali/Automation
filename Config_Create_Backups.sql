DECLARE

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

BEGIN
	
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

END;
/