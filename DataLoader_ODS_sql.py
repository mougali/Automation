#!/usr/local/bin/python2.4

import os, sys, stat
import errno, shutil
import subprocess
import csv

from collections import deque
from subprocess import Popen, PIPE

# Remove directory if exists.
if (os.path.exists("TempProcessing")):
		subprocess.call(['rm', '-r', 'TempProcessing'])

## Loads all data (seed-files) needed for automating the configuration process.

# Commented out while developing
# SUB_DSC = raw_input("Please enter Subscriber Name: ")
# SUB_NM = raw_input("Please enter 3-letter Subscriber Acronym: ")
# SUB_ID = raw_input("Please enter Subscriber ID: ")

SUB_DSC = "WALMART"
SUB_NM = "WAL"
SUB_ID = 55
pre_ods=os.getcwd()+"/ODS/"
pre_gka=os.getcwd()+"/GKA/"
processDate="20150914"
processDate_text="11sep2015"
newProcessDate="20151112"
newProcessDate_text="12nov2015"
suffix=".csv"

# Standards files (.csv's enlisting default/required data for each seed-file)
objGrpStandardsFile = os.getcwd()+"/Resources/OBJ_GRP_STANDARD.csv"
sbjAreaStandardsFile = os.getcwd()+"/Resources/SBJ_AREA_STANDARD.csv"
# natKeyStandardsFile = os.getcwd()+"/Resources/NAT_KEY_STANDARD.csv"
# subDimNatStandardsFile = os.getcwd()+"/Resources/SUB_DIM_NAT_STANDARD.csv"
# natKeyStandardsFile_SCD = os.getcwd()+"/Resources/NAT_KEY_SCD_STANDARD.csv"

# # Temporary standards files (needed to modify data values for each new run)
# temp_natKeyStandardsFile = os.getcwd()+"/TempProcessing/NAT_KEY_STANDARD_"+newProcessDate+".csv"
# temp_subDimNatStandardsFile = os.getcwd()+"/TempProcessing/SUB_DIM_NAT_STANDARD_"+newProcessDate+".csv"

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

# # Table information for GKA
# subTable="SUB_LOYALTYTEST"
# subDimNatKeyTable="SUB_DIM_NAT_KEY_TYP_LOYALTYTEST"

# seed-file info (TEMPORARY)
subSeedName="TMPL_SUB_DATA_20150914.csv"

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

# gkaSeedfileLocations = [pre_gka + "TMPL_DIM_DATA_" + processDate + suffix,
# 						pre_gka + "TMPL_NAT_KEY_TYP_DATA_" + processDate + suffix,
# 						pre_gka + "TMPL_SUB_DATA_" + processDate + suffix,
# 						pre_gka + "TMPL_SUB_DIM_NAT_KEY_TYP_DATA_" + processDate + suffix]


# Make directory for temporary Files (only works in Python >= 3.2)
# os.makedirs(path, exist_ok=True)

# Make directory for temporary files
# Otherwise, use:
def mkdir_p(path):
    # try:
    #     os.makedirs(path)
    # except OSError as exc: # Python >2.5
    #     if exc.errno == errno.EEXIST and os.path.isdir(path):
    #         pass
    #     else: raise
    os.makedirs(path)

path=os.getcwd()+"/TempProcessing/"
mkdir_p(path)

# Duplicate files and insert into new temp path
# Generate file objects for each copied seedfile and
# add to the respective file array

odsFiles = list()
# gkaFiles = list()

# Copy original file contents into temporary production/processing files.
# Store locations of temp-files in ods and gka lists.
for seedfile in odSeedfileLocations:
	seedfileName=seedfile.split('/')[-1]

	# Modify name to describe new processing date
	seedfileName = seedfileName.replace(processDate, newProcessDate)
	shutil.copy2(seedfile, path+seedfileName)

	# Unsafe to keep files open
	# odsFiles.append(open(path+seedfileName))
	odsFiles.append(path+seedfileName)

# for seedfile in gkaSeedfileLocations:
# 	seedfileName=seedfile.split('/')[-1]

# 	# Modify name to describe new processing date
# 	seedfileName = seedfileName.replace(processDate, newProcessDate)
# 	shutil.copy2(seedfile, path+seedfileName)

# 	# Unsafe programming practice to keep files open
# 	# gkaFiles.append(open(path+seedfileName))
# 	gkaFiles.append(path+seedfileName)

# # Generate temporary duplicates of standards-files
# shutil.copy2(natKeyStandardsFile, temp_natKeyStandardsFile)
# shutil.copy2(subDimNatStandardsFile, temp_subDimNatStandardsFile)

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

# Makes file at path executable (modifies user-permissions)
def make_exec(path):
	mode = os.stat(path).st_mode
	os.chmod(path, mode | stat.S_IEXEC)

# # Append record to TMPL_SUB_DATA_20150914.csv (in gkaFiles[2])
# def add_sub_data(subscriberDataFile):
# 	# Parameter 'a' signifies to writer that it should append to file
# 	f = open(subscriberDataFile, 'a')
# 	csvWriter = csv.writer(f, quoting=csv.QUOTE_ALL)
# 	csvWriter.writerow([SUB_ID,SUB_NM,SUB_DSC])
# 	f.close()

# Append record to TMPL_OBJ_GRP_DATA (in odsFiles[2])
def add_obj_grp_data(objGrpDataFile, standardsFile):

	stdFile = open(standardsFile)		# read-only
	outFile = open(objGrpDataFile,'a')	# write-file (being appended)

	reader = csv.reader(stdFile)
	writer = csv.writer(outFile, quoting=csv.QUOTE_NONE)

	for row in reader:
		writer.writerow([SUB_NM,row[0],row[1],row[2],row[3]])

	stdFile.close()
	outFile.close()

def add_sbj_area_data(sbjAreaDataFile, standardsFile):

	stdFile = open(standardsFile)		# read-only
	outFile = open(sbjAreaDataFile,'a')	# write-file (being appended)

	reader = csv.reader(stdFile)
	writer = csv.writer(outFile,quoting=csv.QUOTE_NONE,lineterminator='\n')

	for row in reader:
		writer.writerow([SUB_NM,row[0],row[1],row[2],row[3],row[4],row[5],row[6],""])

	stdFile.close()
	outFile.close()

# Find and return last row of given file
# @param csv_filename CSV file from which final row should be obtained
def get_last_row(csv_filename):
	f = open(csv_filename, 'rb')
	reader = csv.reader(f,delimiter=',')
	return deque(reader).pop()

	# Python >= 2.7 only
	# with open(csv_filename, 'rb') as f:
	# 	return deque(csv.reader(f), 1)[0]

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

# MAIN SCRIPT
# Currently able to write out standard/default values for SUBSCRIBER, OBJECT_GROUPS, and SUBJECT_AREAS
# ADDENDUM 10/26/15: Also writing out default values for TMPL_NAT_KEY_DATA, TMPL_SUB_DIM_NAT_KEY_DATA
def main():

	# add_sub_data(gkaFiles[2])

	add_obj_grp_data(odsFiles[2],objGrpStandardsFile)
	add_sbj_area_data(odsFiles[5],sbjAreaStandardsFile)

	# objGrpScriptPath = os.getcwd()+"/ODS/objGroupFiller.sh"
	# # Change file permission to "Execute by Owner"
	# make_exec(objGrpScriptPath)
	# subprocess.call([objGrpScriptPath, SUB_NM, SUB_ID])

	# Clean-up
	# closeDeleteFiles(odsFiles)
	# closeDeleteFiles(gkaFiles)
	# os.rmdir(path)

	# Only works in dev-environment
	# pushSeedData("GKA")
	pushSeedData("ODS")

	date="16nov2015"
	SRC_CD="WAL"
	SRC_DSC="WALMART"
	SRC_ID="55"
	CKA_SUB_NM="WAL"
	CKA_SUB_ID="55"
	CLNT_CD="WAL"
	CLNT_DSC="WALMART"
	CLNT_ID="21"

	platformID = raw_input("Please specify PLATFORM ID: ")
	connectionID = int(platformID)*10
	connectionID = str(connectionID)

	paramList = (date, SRC_CD, SRC_DSC, SRC_ID, CKA_SUB_NM, CKA_SUB_ID, CLNT_CD, CLNT_DSC, CLNT_ID)
	connectParams = inputConnectionDetails()

	cmd = ["sqlplus", od_connectionParam, "@CIF_Config_Parameterized.sql"]
	cmd += paramList
	cmd += connectParams
	cmd += (platformID, connectionID)
	print cmd

	# Call CIF_Config.sql
	# Used to setup platform and connection details for client.
	# subprocess.call(['sqlplus', '-S', od_connectionParam, '@CIF_Config_Parameterized.sql', paramList[0], paramList[1], paramList[2], paramList[3], paramList[4], paramList[5], paramList[6], paramList[7], paramList[8], connectParams[0], connectParams[1], connectParams[2], connectParams[3], connectParams[4], connectParams[5], platformID, connectionID])

	# subprocess.call(['sqlplus', '-S', od_connectionParam, '@CIF_Config_Parameterized.sql', paramList, connectParams, platformID, connectionID])
	
	addOrDrop = raw_input("Add data (Y) or Drop data (N)? --> ")
	if (addOrDrop == "Y"):
		subprocess.call(cmd)
	elif (addOrDrop == "N"):
		cmd[2] = "@removeAddendums.sql"
		subprocess.call(cmd)

	# MUST LOGIN TO GKA BEFORE TRIGGERING THIS SCRIPT
	# Trigger cka_config_data_load.ksh to output to CKA DB
	# subprocess.call([ckaDataLoad_script,processDate])

	# Trigger tlog_config_data_load.ksh to output to ODconfig
	# subprocess.call([odsDataLoad_script,newProcessDate])

if __name__ == '__main__':
	main()