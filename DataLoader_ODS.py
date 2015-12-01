#!/usr/local/bin/python2.4

import os, sys, stat
import errno, shutil
import subprocess
import csv
import glob

from collections import deque
from subprocess import Popen, PIPE

## Loads all data (seed-files) needed for automating the configuration process.

# Commented out while developing
# SRC_DSC = raw_input("Please enter Subscriber Name: ")
# SRC_CD = raw_input("Please enter 3-letter Subscriber Acronym: ")
# SRC_ID = raw_input("Please enter Subscriber ID: ")

SRC_DSC = "WALMART"
SRC_CD = "WAL"
SRC_ID = 55
pre_ods=os.getcwd()+"/ODS/"
pre_gka=os.getcwd()+"/GKA/"
processDate="20150914"
processDate_text="11sep2015"
newProcessDate="20151112"
newProcessDate_text="12nov2015"
suffix=".csv"

date="16nov2015"

# Standards files (.csv's enlisting default/required data for each seed-file)
objStdFile = os.getcwd()+"/Resources/OBJ_STANDARD.csv"
objGrpStandardsFile = os.getcwd()+"/Resources/OBJ_GRP_STANDARD.csv"
sbjAreaStandardsFile = os.getcwd()+"/Resources/SBJ_AREA_STANDARD.csv"

# SQL scripts
dropRecreateTablesScript = os.getcwd()+"/CIF_Seedfile_Config_load.sql"

# Login information for databases and environments
# To-Do: ROUTE PASSWORD INPUT THROUGH ODconfig
userGKA="AODR45CKAADVD"
passwordGKA="ckaadvaodr5dev"
sidGKA="CKA280D"
connectionString=userGKA+"/"+passwordGKA+"@"+sidGKA

# Set login credentials (for ODconfig)
userODS = 'AODR45ODCONFIGD'
pwdODS = 'odconfigaodr5dev'
sidODS = 'CMI280D'
schemaODS = 'AODR45ODCONFIGD'
od_connectionParam=userODS+"/"+pwdODS+"@"+sidODS

connectionLiteral = "AODR45ODCONFIGD/odconfigaodr5dev@CMI280D"

# Command to initiate and connect to SQL*PLUS
# sqlplus -S AODR45CKAADVD/ckaadvaodr5dev@CKA280D
# End login information

# Other parameters
geolocation = "US"		# USA is default value

# DIRECTORY VARIABLES
CKA_CODEBASE_KSH="/dsd_2/relr45d/ckaadv/code/bin/"
CKA_CODEBASE_PYTHON="/dsd_2/relr45d/ckaadv/code/python/"
GKA_INPUT_DEST="/dsd_2/relr45d/ckaadv/data/inputs/config/"

ODS_CODEBASE_KSH="/dsd_2/relr45d/tlog/code/bin/"
ODS_INPUT_DEST="/dsd_2/relr45d/tlog/data/inputs/config/"

# Shell-scripts
ckaDataLoad_script=CKA_CODEBASE_KSH+"cka_config_data_load.ksh"
odsDataLoad_script=ODS_CODEBASE_KSH+"tlog_config_data_load.ksh"

odSeedfileLocations =  [pre_ods + "TMPL_CUST_ADAPT_" + processDate + suffix,
						pre_ods + "TMPL_OBJ_DATA_" + processDate + suffix, 
						pre_ods + "TMPL_OBJ_GRP_DATA_" + processDate + suffix,
						pre_ods + "TMPL_OBJ_PRCS_EXCPN_" + processDate + suffix,
						pre_ods + "TMPL_PRCS_CFG_" + processDate + suffix,
						pre_ods + "TMPL_SBJ_AREA_DATA_" + processDate + suffix,
						pre_ods + "TMPL_SUB_DIM_KEY_DATA_" + processDate + suffix,
						pre_ods + "TMPL_STD_FMT_META_DATA_" + processDate + suffix,
						pre_ods + "TMPL_SRVC_ORCH_DATA_" + processDate + suffix,
						pre_ods + "TMPL_DIM_DATA_" + processDate + suffix]

# **********END VARIABLE INIT**************


# Make directory for temporary files
def mkdir_p(path):
    # try:
    #     os.makedirs(path)
    # except OSError as exc: # Python >2.5
    #     if exc.errno == errno.EEXIST and os.path.isdir(path):
    #         pass
    #     else: raise
    os.makedirs(path)

# Makes file at path executable (modifies user-permissions)
def make_exec(path):
	mode = os.stat(path).st_mode
	os.chmod(path, mode | stat.S_IEXEC)

# Set all items needed for startup/initialization 
def initStartup():
	path=os.getcwd()+"/TempProcessing/"
	
	# Remove directory if exists.
	if (os.path.exists("TempProcessing")):
		subprocess.call(['rm', '-r', 'TempProcessing'])
	
	# Make directory
	mkdir_p(path)

	# List containing locations of new versions of seed-files (w/ new process dates)
	# NOTE: These are not the files themselves, just the path locations
	odsFiles = list()

	# Copy original file contents into temporary production/processing files.
	# Store locations of temp-files in ods and gka lists.
	for seedfile in odSeedfileLocations:
		seedfileName=seedfile.split('/')[-1]

		# Modify name to describe new processing date
		seedfileName = seedfileName.replace(processDate, newProcessDate)
		
		# Copy new version (w/ updated process date) of seed-file
		# to the new path
		shutil.copy2(seedfile, path+seedfileName)

		odsFiles.append(path+seedfileName)


# Back-up original seedfiles in data/inputs/config/
# @param seedfileDirectory - Location/Directory of seedfiles in the environment.
# @param processDate - Date suffix of seedfile names. Used in naming of backup directory.
def backupSeedFiles(seedfileDirectory, processDate):

	# Make directory (named after processDate in YYYYMMDD) if doesn't exist
	path=os.path.join(seedfileDirectory, processDate+"_BKP")
	if not os.path.exists(path):
		os.makedirs(path)

	# regexStr=r'*'+processDate
	# print glob.glob(seedfileDirectory+regexStr)

	# # Find and move the relevant seedfiles
	# for seedcsv in glob.glob(r'*'+processDate+'.csv'):
	# 	# Push original seedfiles into path
	# 	shutil.move(seedcsv, path)

	stmnt="mv "+seedfileDirectory+"*"+processDate+".csv"+" "+path
	subprocess.call(stmnt, shell=True)

# Be sure to delete path at the end of program processing
def closeDeleteFiles(filesArr):
	# try:
	# 	for filename in filesArr:
	# 		# Close file before removing (if it's not already closed)
	# 		if not (filename.closed):
	# 			filename.close()
	# 		os.remove(filename.name)
	# except OSError as exc:
	# 	if exc.errno == errno.EEXIST:
	# 		pass
	# 	else: raise
	for filename in filesArr:
			# Close file before removing (if it's not already closed)
			if not (filename.closed):
				filename.close()
			os.remove(filename.name)

# Append default records to TMPL_OBJ_DATA
# @param objDataFile - CSV file to output to.
# @param standardsFile - File to input from.
def add_obj_data(objDataFile, standardsFile):

	stdFile = open(standardsFile)		# read-only
	outFile = open(objDataFile, 'a')	# write-file (being appended)

	reader = csv.reader(stdFile)
	writer = csv.writer(outFile, quoting=csv.QUOTE_NONE, lineterminator=os.linesep)

	for row in reader:
		
		paramList = [SRC_CD, ]
		paramList += row

		# If datafile contains reference to SRC_CD (3-letter acronym),
		# ensure that record being output to DB contains the appropriate name.
		if ("***" in paramList[10]):
			paramList[10] = paramList[10].replace("***", SRC_CD)	

		writer.writerow(paramList)

	stdFile.close()
	outFile.close()

# Append record to TMPL_OBJ_GRP_DATA (in odsFiles[2])
def add_obj_grp_data(objGrpDataFile, standardsFile):

	stdFile = open(standardsFile)		# read-only
	outFile = open(objGrpDataFile,'a')	# write-file (being appended)

	reader = csv.reader(stdFile)
	writer = csv.writer(outFile, quoting=csv.QUOTE_NONE)

	for row in reader:
		writer.writerow([SRC_CD,row[0],row[1],row[2],row[3]])

	stdFile.close()
	outFile.close()

# Append records to TMPL_SBJ_AREA_DATA
def add_sbj_area_data(sbjAreaDataFile, standardsFile):

	stdFile = open(standardsFile)		# read-only
	outFile = open(sbjAreaDataFile,'a')	# write-file (being appended)

	reader = csv.reader(stdFile)
	writer = csv.writer(outFile,quoting=csv.QUOTE_NONE,lineterminator='\n')

	for row in reader:
		writer.writerow([SRC_CD,row[0],row[1],row[2],row[3],row[4],row[5],row[6],""])

	stdFile.close()
	outFile.close()

# Append records to TMPL_PRCS_CFG
# All records are generally the same, in the format: SUB_CD, 'N', '600'
# @param prcsCfgDataFile - Path of seedfile to be appended
# @param standardsFile - Path of file to be read from (used as data input)
def add_prcs_cfg_data(prcsCfgDataFile, standardsFile):

# Append records to TMPL_OBJ_PRCS_EXCPN
# @param objPrcsExcpnFile - Path of seedfile to be appended
# @param standardsFile - Path of file to be read from (used as data input)
def add_obj_prcs_excpn_data(objPrcsExcpnFile, standardsFile):

# Append records to TMPL_OBJ_PRCS_EXCPN
# @param objPrcsExcpnFile - Path of seedfile to be appended
# @param standardsFile - Path of file to be read from (used as data input)
def add_cust_adapt_data(custAdaptFile, standardsFile):

# Find and return last row of given file
# @param csv_filename CSV file from which final row should be obtained
def get_last_row(csv_filename):
	f = open(csv_filename, 'rb')
	reader = csv.reader(f,delimiter=',')
	return deque(reader).pop()

# Generate SQL file for GKA database
# @param tableName
# @param seed-file
def createGkaQuery(tableName, seedFile):

	# Call helper method
	queryResult, errors = getColNames(tableName)

# Get column names for given table
# Helper function for createGkaQuery
# @param tableName
def getColNames(tableName):
	# Pseudocode
	# 1) connect to GKA database
	# 2) Use DB connection details to formulate command string
	# 3) Issue command using subprocess.Popen(). Store stdout, stderror in vars.
	# 4) Send SQL query to receive column-names

	connectionParam=userGKA+"/"+passwordGKA+"@"+sidGKA

	session = subprocess.Popen(['sqlplus', '-S', connectionParam], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderror=subprocess.PIPE)
	stdout, stderr = process.communicate()

	sqlQuery="SELECT column_names FROM USER_TAB_COLUMNS WHERE table_name = \'" + tableName + "\'"

	session.stdin.write(sqlQuery)

	# Returns a tuple
	# e.g:
	# stdout, stderror = session.communicate()
	return session.communicate()

# Backup tables in GKA databse
# DOES cka_config_data_load.ksh backup tables?
def backup_tables_GKA():
	# NEEDS MODIFICATION (results in error in interpreter)
	sql_query="create table sub_bkp_"+processDate_text+" as select * from sub;create table nat_key_typ_bkp_"+processDate_text+" as select * from nat_key_typ;create table dim_bkp_"+processDate_text+" as select * from dim;create table sub_dim_nat_key_typ_"+processDate_text+" as select * from sub_dim_nat_key_typ;"

# Get column names for given table
# Helper function for createGkaQuery
# @param tableName
def getColNames(tableName):
	# Pseudocode
	# 1) connect to GKA database
	# 2) Use DB connection details to formulate command string
	# 3) Issue command using subprocess.Popen(). Store stdout, stderror in vars.
	# 4) Send SQL query to receive column-names

	connectionParam=userGKA+"/"+passwordGKA+"@"+sidGKA

	# Query-Flags to suppress all output other than values
	sqlQueryFlags="SET PAGESIZE 0 FEEDBACK OFF VERIFY OFF HEADING OFF ECHO OFF\n"
	sqlQuery=sqlQueryFlags+"SELECT column_name FROM USER_TAB_COLUMNS WHERE table_name = \'" + tableName + "\';"

	queryResult, errors = runSqlQuery(sqlQuery, connectionParam)

	# Returns a tuple
	# e.g:
	# stdout, stderror = session.communicate()
	return queryResult

# Send GKA-files from TempProcessing/ to default storage folder.
# Files are accessed by cka_config_data_load.ksh here for formulation of SQL Insert queries.
# Throws exception if ODS seedfiles are being pushed to the wrong directory.
# Throws exception if GKA seedfiles are being pushed to the wrong directory.
# @param seedfileType- Option specifying which seedfiles to push ("GKA" or "ODS")
def pushSeedData(seedfileType=None):

	if (seedfileType==None):
		print "No seedfiles were specified."
	elif (seedfileType=="GKA"):
		for row in gkaFiles:
			subprocess.call(["mv",row,GKA_INPUT_DEST])
	elif (seedfileType=="ODS"):
		for row in 	odsFiles:
			subprocess.call(["mv",row,ODS_INPUT_DEST])

# returns a tuple specifying values for:
# NTZ_ODS_STG_SVR
# NTZ_ODS_STG_UID
# NTZ_ODS_STG_DB
# NTZ_ODS_STG_PW
# NTZ_ODS_ODS_DB
# NTZ_ODS_CKR_DB
# @return 6-fold tuple containing the above information.
def inputConnectionDetails():
	print("PLEASE ENTER THE FOLLOWING PARAMS FOR CONNECTION-DETAILS")

	# Temporarily commented out for automated testing.
	# connectDetails = ()
	# connectDetails += (raw_input("Specify the NTZ_ODS_STG_SVR: "),)
	# connectDetails += (raw_input("Specify the NTZ_ODS_STG_UID: "),)
	# connectDetails += (raw_input("Specify the NTZ_ODS_STG_DB: "),)
	# connectDetails += (raw_input("Specify the NTZ_ODS_STG_PW: "),)
	# connectDetails += (raw_input("Specify the NTZ_ODS_ODS_DB: "),)
	# connectDetails += (raw_input("Specify the NTZ_ODS_CKR_DB: "),)

	connectDetails = ("NANTZ85.NIELSEN.COM", "AODR1Q85", "AODR1Q_LC2_TLOG_STG", "AOD85", "AODR1Q_LC2_TLOG_ODS", "AODR1Q_CKR_ADV")

	return connectDetails

# Function that takes the sqlCommand and connectString and returns the queryResult and errorMessage (if any)
# CREDIT: https://moizmuhammad.wordpress.com/2012/01/31/run-oracle-commands-from-python-via-sql-plus/
def runSqlQuery(paramList):

	params = ['sqlplus', '-S', ]
	params += paramList
	session = Popen(params, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	return session.communicate()	

# MAIN SCRIPT
# Currently able to write out standard/default values for SUBSCRIBER, OBJECT_GROUPS, and SUBJECT_AREAS
# ADDENDUM 10/26/15: Also writing out default values for TMPL_NAT_KEY_DATA, TMPL_SUB_DIM_NAT_KEY_DATA
def main():

	# Perform house-cleaning activities needed for startup
	initStartup()

	# Backup files
	backupSeedFiles(ODS_INPUT_DEST, processDate)

	# add_sub_data(gkaFiles[2])

	add_obj_grp_data(odsFiles[2],objGrpStandardsFile)
	add_obj_data(odsFiles[1], objStdFile)
	add_sbj_area_data(odsFiles[5],sbjAreaStandardsFile)

	# objGrpScriptPath = os.getcwd()+"/ODS/objGroupFiller.sh"
	# # Change file permission to "Execute by Owner"
	# make_exec(objGrpScriptPath)
	# subprocess.call([objGrpScriptPath, SRC_CD, SRC_ID])

	# Clean-up
	# closeDeleteFiles(odsFiles)
	# closeDeleteFiles(gkaFiles)
	# os.rmdir(path)

	# Only works in dev-environment
	# pushSeedData("GKA")
	pushSeedData("ODS")

	# SRC_CD="WAL"
	# SRC_DSC="WALMART"
	# SRC_ID="55"
	CKA_SRC_CD="WAL"
	CKA_SRC_ID="55"
	CLNT_CD="WAL"
	CLNT_DSC="WALMART"
	CLNT_ID="21"

	platformID = raw_input("Please specify PLATFORM ID: ")
	connectionID = int(platformID)*10
	connectionID = str(connectionID)

	paramList = (date, SRC_CD, SRC_DSC, SRC_ID, CKA_SRC_CD, CKA_SRC_ID, CLNT_CD, CLNT_DSC, CLNT_ID)
	connectParams = inputConnectionDetails()

	# Generate SQL command to run CIF_Config_Parameterized.sql,
	# complete with needed parameters.
	cmd = [od_connectionParam, "@CIF_Config_Parameterized.sql"]
	cmd += paramList
	cmd += connectParams
	cmd += (platformID, connectionID)

	dropRecreateParams = [od_connectionParam, "@"+dropRecreateTablesScript]

	addOrDrop = raw_input("Add data (Y) or Drop data (N)? --> ")
	if (addOrDrop == "Y"):
		runSqlQuery(dropRecreateParams)
		runSqlQuery(cmd)
		subprocess.call([odsDataLoad_script,newProcessDate])
	elif (addOrDrop == "N"):
		cmd[1] = "@removeAddendums.sql"		
		runSqlQuery(cmd)

if __name__ == '__main__':
	main()