DECLARE
	v_stmt_drop1 VARCHAR2(500) := 'DROP TABLE PLATFORM_STCK_BKP_&1';
	v_stmt_drop2 VARCHAR2(500) := 'DROP TABLE PLATFORM_DTL_BKP_&1';
	v_stmt_drop3 VARCHAR2(500) := 'DROP TABLE CONNECTION_DETAILS_&1';
	v_stmt_drop4 VARCHAR2(500) := 'DROP TABLE PROP_CNTNT_BKP_&1';
	v_stmt_drop5 VARCHAR2(500) := 'DROP TABLE OPT_TAB_COL_BKP_&1';
	v_stmt_drop6 VARCHAR2(500) := 'DROP TABLE SRC_BKP_&1';
	v_stmt_drop7 VARCHAR2(500) := 'DROP TABLE CLNT_BKP_&1';
	v_stmt_drop8 VARCHAR2(1000) := 'DROP TABLE PRCS_CONF_&1';
	v_stmt_drop9 VARCHAR2(1000) := 'DROP TABLE OBJ_GRP_&1';
	v_stmt_drop10 VARCHAR2(1000) := 'DROP TABLE SBJ_AREA_&1';
	v_stmt_drop11 VARCHAR2(1000) := 'DROP TABLE OBJ_&1';
	v_stmt_drop12 VARCHAR2(1000) := 'DROP TABLE DIM_&1';
	v_stmt_drop13 VARCHAR2(1000) := 'DROP TABLE STD_FMT_META_DTA_&1';
	v_stmt_drop14 VARCHAR2(1000) := 'DROP TABLE SRVC_ORCH_&1';
	v_stmt_drop15 VARCHAR2(1000) := 'DROP TABLE OBJ_PRCS_EXCPN_&1';
	v_stmt_drop16 VARCHAR2(1000) := 'DROP TABLE CUST_ADAPT_&1';
	v_stmt_drop17 VARCHAR2(1000) := 'DROP TABLE SUB_DIM_KEY_&1';

	v_stmt_removeRec VARCHAR2(500) := 'DELETE FROM PLATFORM_STCK WHERE PLTFM_ID = &16';

	var_platformID NUMBER(10, 0) := &16;
	-- var_platformIdProp matches the data definition in the PROP_CNTN table; contains same value as var_platformID
	var_platformIdProp NUMBER(20, 0) := &16;
	var_connectionID NUMBER(10, 0) := &17;
	var_platformDesc VARCHAR2(100 BYTE) := '&2';
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
	EXECUTE IMMEDIATE v_stmt_drop1;
	EXECUTE IMMEDIATE v_stmt_drop2;	
	EXECUTE IMMEDIATE v_stmt_drop3;
	EXECUTE IMMEDIATE v_stmt_drop4;
	EXECUTE IMMEDIATE v_stmt_drop5;
	EXECUTE IMMEDIATE v_stmt_drop6;
	EXECUTE IMMEDIATE v_stmt_drop7;
	EXECUTE IMMEDIATE v_stmt_drop8;
	EXECUTE IMMEDIATE v_stmt_drop9;	
	EXECUTE IMMEDIATE v_stmt_drop10;
	EXECUTE IMMEDIATE v_stmt_drop11;
	EXECUTE IMMEDIATE v_stmt_drop12;
	EXECUTE IMMEDIATE v_stmt_drop13;
	EXECUTE IMMEDIATE v_stmt_drop14;
	EXECUTE IMMEDIATE v_stmt_drop15;
	EXECUTE IMMEDIATE v_stmt_drop16;
	EXECUTE IMMEDIATE v_stmt_drop17;
	COMMIT;

	EXECUTE IMMEDIATE v_stmt_removeRec;
	COMMIT;

	/* DELETE records from PLATFORM_DTL table */
	v_stmt_removeRec := 'DELETE FROM PLATFORM_DTL WHERE PLTFM_ID = :g_pID';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_platformID;
	COMMIT;

	v_stmt_removeRec := 'DELETE FROM PLATFORM_DTL WHERE PLTFM_ID = :g_pID AND CONNECTION_ID = :g_cID';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_platformID, var_connectionID;
	COMMIT;

	/* DELETE from CONNECTION_DETAILS table */
	v_stmt_removeRec := q'$DELETE FROM CONNECTION_DETAILS WHERE CONNECTION_ID = :c_ID AND PARAMETER_VALUE = :pVal$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_connectionID, var_ntzServ;
	COMMIT;

	v_stmt_removeRec := q'$DELETE FROM CONNECTION_DETAILS WHERE CONNECTION_ID = :c_ID AND PARAMETER_VALUE = :pVal$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_connectionID, var_ntzUID;
	COMMIT;

	v_stmt_removeRec := q'$DELETE FROM CONNECTION_DETAILS WHERE CONNECTION_ID = :c_ID AND PARAMETER_VALUE = :pVal$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_connectionID, var_ntzDB;
	COMMIT;

	v_stmt_removeRec := q'$DELETE FROM CONNECTION_DETAILS WHERE CONNECTION_ID = :c_ID AND PARAMETER_VALUE = :pVal$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_connectionID, var_ntzPW;
	COMMIT;

	v_stmt_removeRec := q'$DELETE FROM CONNECTION_DETAILS WHERE CONNECTION_ID = :c_ID AND PARAMETER_VALUE = :pVal$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_connectionID, var_ntzOdsDB;
	COMMIT;

	v_stmt_removeRec := q'$DELETE FROM CONNECTION_DETAILS WHERE CONNECTION_ID = :c_ID AND PARAMETER_VALUE = :pVal$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_connectionID, var_ntzCkrDB;
	COMMIT;

	/* DELETE from PROP_CNTNT all appended values (based on SOURCE_ID and PLATFORM_ID) */
	v_stmt_removeRec := q'$DELETE FROM PROP_CNTNT WHERE SOURCE_ID = :g_srcID AND PLATFORM_ID = :g_pID$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_srcID, var_platformIdProp;
	COMMIT;

	/* DELETE from SRC all appended values (based on SRC_ID and SRC_CD) */
	v_stmt_removeRec := q'$DELETE FROM SRC WHERE SRC_ID = :g_srcID AND SRC_CD = :g_srcCd$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_srcIdSRC, var_srcCode;
	COMMIT;

	/* DELETE from CLNT all appended values (based on SRC_ID and SRC_CD) */
	v_stmt_removeRec := q'$DELETE FROM CLNT WHERE CLNT_ID = :g_clientID AND CLNT_CD = :g_clientCode$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_clientID, var_clientCode;
	COMMIT;

	/* DELETE from OBJ_GRP all appended values (based on SRC_ID) */
	v_stmt_removeRec := q'$DELETE FROM OBJ_GRP WHERE SRC_ID = :g_srcID$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_srcID;
	COMMIT;

	/* DELETE from OBJ all appended values (based on SRC_ID) */
	v_stmt_removeRec := q'$DELETE FROM OBJ WHERE SRC_ID = :g_srcID$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_srcID;
	COMMIT;

	/* DELETE from SBJ_AREA all appended values (based on SRC_ID) */
	v_stmt_removeRec := q'$DELETE FROM SBJ_AREA WHERE SRC_ID = :g_srcID$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_srcID;
	COMMIT;

	/* DELETE from PRCS_CONF all appended values (based on SRC_ID) */
	v_stmt_removeRec := q'$DELETE FROM PRCS_CONF WHERE SRC_ID = :g_srcID$';
	EXECUTE IMMEDIATE v_stmt_removeRec
		USING var_srcID;
	COMMIT;

END;
/