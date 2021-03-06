#!/usr/local/bin/python2.4

# PROGRAM PREREQUISITES:
# If adding data:
#	Ensure that appropriate seedfiles are present in data/inputs/config/
#	Ensure that most recent date entry in datetimelog.csv matches date of seedfiles in data/inputs/config/

import os, sys, stat
import errno, shutil
import subprocess
import csv
import glob

from collections import deque
from subprocess import Popen, PIPE
from datetime import datetime, date, time

pre_ods=os.getcwd()+"/ODS/"
pre_gka=os.getcwd()+"/GKA/"

origProcessDateObj=''	
origProcessDate=''		# E.g. "20150914"
origProcessDate_text=''	# E.g. "11sep2015"
newProcessDateObj=''
newProcessDate=''
newProcessDate_text=''
suffix=".csv"

# Dictionary containing all input variables.
# Values will be loaded in a later function.
inputDataDict = {}

# Standards files (.csv's enlisting default/required data for each seed-file)
objStdFile = os.getcwd()+"/Resources/OBJ_STANDARD.csv"
objGrpStandardsFile = os.getcwd()+"/Resources/OBJ_GRP_STANDARD.csv"
sbjAreaStandardsFile = os.getcwd()+"/Resources/SBJ_AREA_STANDARD.csv"

# Log-file paths
datelogPath = os.path.join(os.getcwd(),"Resources","datetimelog.csv")				
subIdResourcePath = os.path.join(os.getcwd(),"Resources","datasrc.txt")
datelogPath_backup = ''
subIdResourcePath_backup = ''

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

# INPUT FILE (from order-form)
inputFileName = "OrderForm.csv"
inputFilePath = ""

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

odSeedfileLocations = []

# List that will contain pathnames of all new ODS seedfiles
odsFiles = ()						

# Input parameters
SRC_DSC = ""
SRC_CD = ""
SRC_ID = -1
CKA_SRC_CD =""
CKA_SRC_ID =-1
CLNT_CD = ""
CLNT_DSC = ""
CLNT_ID = -1
platformID = -1
connectionID = -1

# **********END VARIABLE INIT**************


# Load input data from order-form file into a dictionary.
# Assign appropriate variables.
# @param orderFormFile - CSV file containing Parameter Names and Values
def loadInputData(orderFormFile):
	global inputDataDict

	f = open(orderFormFile)
	reader = csv.reader(f)
	reader.next()	# Skip header row

	counter = 0
	for row in reader:
		try:
			key = row[0]
			val = row[1]

			# Raise exceptions if either field is null
			if not key:
				raise ValueError("Key is missing in Record " + str(counter))
			if not val:
				raise ValueError("Value is missing in Record " + str(counter))

			inputDataDict.update({key: val})
			counter += 1
		except IndexError, msg:
			print msg
			print "Please ensure order-form is completely and accurately filled."
			resetOriginalState()
			sys.exit(1)
		except ValueError, msg:
			print msg
			print "Please ensure order-form is completely and accurately filled."
			resetOriginalState()
			sys.exit(1)

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
# loadInputData() - Load input data (from order-form) into dictionary inputDataDict.
# Load values in inputDataDict into global variables (e.g. SRC_CD).
# Copy most recent seedfiles from data/input/config/ into 
# REQUIREMENT: All seedfiles must be existent in data/input/config/
def initStartup():

	# Establish location of order-form based input file
	global inputFilePath
	global inputFileName
	inputFilePath = os.path.join(os.getcwd(), inputFileName)

	# Call loadInputData to establish values for input parameters
	loadInputData(inputFilePath)
	global inputDataDict
	for key, value in inputDataDict.iteritems():
		print key + ": " + value

	# Establish variable names from dictionary
	# Ensure that values are assigned to the global variables
	global SRC_DSC, SRC_CD, SRC_ID, CKA_SRC_CD, CKA_SRC_ID, CLNT_CD, CLNT_DSC, CLNT_ID
	SRC_DSC = inputDataDict["Subscriber Name"]
	SRC_CD = inputDataDict["Subscriber Code"]
	SRC_ID = inputDataDict["Subscriber ID"]
	CKA_SRC_CD = inputDataDict["CKA Subscriber Code"]
	CKA_SRC_ID = inputDataDict["CKA Subscriber ID"]
	CLNT_CD = SRC_CD
	CLNT_DSC= SRC_DSC
	CLNT_ID = "21"	# Dummy value for now (need to pull from sequence in ODconfig CLNT table)

	global platformID, connectionID
	platformID = inputDataDict["Platform ID"]
	connectionID = int(platformID)*10
	connectionID = str(connectionID)

	# Establish locations of original ODS seed-files
	global odSeedfileLocations
	odSeedfileLocations =  [ODS_INPUT_DEST + "TMPL_CUST_ADAPT_" + origProcessDate + suffix,
						ODS_INPUT_DEST + "TMPL_OBJ_DATA_" + origProcessDate + suffix, 
						ODS_INPUT_DEST + "TMPL_OBJ_GRP_DATA_" + origProcessDate + suffix,
						ODS_INPUT_DEST + "TMPL_OBJ_PRCS_EXCPN_" + origProcessDate + suffix,
						ODS_INPUT_DEST + "TMPL_PRCS_CFG_" + origProcessDate + suffix,
						ODS_INPUT_DEST + "TMPL_SBJ_AREA_DATA_" + origProcessDate + suffix,
						ODS_INPUT_DEST + "TMPL_SUB_DIM_KEY_DATA_" + origProcessDate + suffix,
						ODS_INPUT_DEST + "TMPL_STD_FMT_META_DATA_" + origProcessDate + suffix,
						ODS_INPUT_DEST + "TMPL_SRVC_ORCH_DATA_" + origProcessDate + suffix,
						ODS_INPUT_DEST + "TMPL_DIM_DATA_" + origProcessDate + suffix]

# Load previous processing date and new date into global vars.
# @param datetimelogFilePath - Path of datetimelog.csv (stores previous processing datetimes)
def loadDates(datetimelogFilePath):
	global origProcessDateObj, origProcessDate, origProcessDate_text
	global newProcessDateObj, newProcessDate, newProcessDate_text

	# set current datetime variables
	newProcessDateObj = datetime.today()
	newProcessDate = newProcessDateObj.strftime('%Y%m%d')
	newProcessDate_text = newProcessDateObj.strftime('%d%b%Y').lower()	# e.g. "12nov2015"

	# load file at datetimelogFilePath
	f = open(datetimelogFilePath, 'rb')
	reader = csv.reader(f)
	params = deque(reader)[-1]	# Get last record in file
	f.close()
	p1, p2, p3, p4, p5, p6 = params
	p1 = int(p1)
	p2 = int(p2)
	p3 = int(p3)
	p4 = int(p4)
	p5 = int(p5)
	p6 = int(p6)

	# Create original processing datetime object.
	origProcessDateObj = datetime(p1,p2,p3,p4,p5,p6)
	origProcessDate = origProcessDateObj.strftime('%Y%m%d')
	origProcessDate_text = origProcessDateObj.strftime('%d%b%Y').lower()

# Append new processing-date to logfile
# @param datetimelogFilePath - Location of logfile being appended.
# @param isInsert - true if user wants to append record, false if user wants to remove record 
def updateDates(datetimelogFilePath, isInsert):
	if isInsert:
		f = open(datetimelogFilePath, 'a')
		writer = csv.writer(f,quoting=csv.QUOTE_NONE,lineterminator=os.linesep)
		dateOutput=newProcessDateObj.strftime('%Y,%m,%d,%H,%M,%S')
		dateOutputTuple=tuple(dateOutput.split(','))
		writer.writerow(dateOutputTuple)
		f.close()
	else:
		# Read contents of file, store in variable 'records'
		readFile = open(datetimelogFilePath)
		records = readFile.readlines()
		readFile.close()

		# Write all records except final record into file
		writeFile = open(datetimelogFilePath, 'w')
		writeFile.writelines([item for item in records[:-1]])
		writeFile.close()

# Refreshes the datasrc file containing subscriber records in SRC table of ODconfig.
# Adds currently processing subscriber to the datasrc file.
# This file is used as a data-source in Sheet 2 of OrderFormTemplate.csv.
# @param subLogFile - Location of file containing all existent Subscribers (SRC_DSC and SRC_ID)
def updateOrderFormInfo(subLogFile):
	if os.path.exists(subLogFile):
		f = open(subLogFile, 'a')
		writer = csv.writer(f,quoting=csv.QUOTE_NONE,lineterminator=os.linesep)
		writer.writerow([SRC_DSC,SRC_ID])
		f.close()
	else:
		raise IOError("Subscriber log-file was not found.")		

# Copies original seedfiles (from /data/inputs/config/) into TempProcessing/.
# The copied seedfiles will be appended to with new records.
def copyOrigSeedfiles():
	
	path=os.getcwd()+"/TempProcessing/"
	
	# Remove directory if exists.
	if (os.path.exists("TempProcessing")):
		subprocess.call(['rm', '-r', 'TempProcessing'])
	
	# Make directory
	mkdir_p(path)

	# List containing locations of new versions of seed-files (w/ new process dates)
	# NOTE: These are not the files themselves, just the path locations
	global odsFiles
	odsFiles = list()

	# Copy original file contents into temporary production/processing files.
	# Store locations of temp-files in ods and gka lists.
	for seedfile in odSeedfileLocations:

		seedfileName=seedfile.split('/')[-1]

		# Modify name to describe new processing date
		seedfileName = seedfileName.replace(origProcessDate, newProcessDate)
		
		# Copy new version (w/ updated process date) of seed-file to the new path
		# Throw errors if all specified seed-files don't exist in source directory
		# or if source == destination. 
		try: 
			shutil.copy2(seedfile, path+seedfileName)
		except shutil.Error, msg:
			print msg
			print "Please ensure that source is not same as destination."
			resetOriginalState()
			sys.exit(1)
		except IOError, msg:
			print msg
			print "Please ensure that all required seed-files exist in source (data/inputs/config/)."
			resetOriginalState()
			sys.exit(1)

		odsFiles.append(path+seedfileName)

# Back-up original seedfiles in data/inputs/config/
# @param seedfileDirectory - Location/Directory of seedfiles in the environment.
# @param origProcessDate - Date suffix of seedfile names. Used in naming of backup directory.
def backupSeedFiles(seedfileDirectory, origProcessDate):

	# Make directory (named after origProcessDate in YYYYMMDD) if doesn't exist
	destination=os.path.join(seedfileDirectory, origProcessDate+"_BKP")
	if not os.path.exists(destination):
		os.makedirs(destination)

	# Get list of files in seedfileDirectory
	files = os.listdir(seedfileDirectory)

	# Move all relevant files (with original process-date) into backup folder
	for f in files:
		if f.endswith(origProcessDate+".csv"):
			try:
				shutil.move(os.path.join(seedfileDirectory,f), destination)
			except IOError, msg:
				print IOError
				print msg
				resetOriginalState()
				sys.exit(1)

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
	writer = csv.writer(outFile, quoting=csv.QUOTE_NONE, lineterminator=os.linesep)

	for row in reader:
		writer.writerow([SRC_CD,row[0],row[1],row[2],row[3]])

	stdFile.close()
	outFile.close()

# Append records to TMPL_SBJ_AREA_DATA
def add_sbj_area_data(sbjAreaDataFile, standardsFile):

	stdFile = open(standardsFile)		# read-only
	outFile = open(sbjAreaDataFile,'a')	# write-file (being appended)

	reader = csv.reader(stdFile)
	writer = csv.writer(outFile,quoting=csv.QUOTE_NONE,lineterminator=os.linesep)

	for row in reader:
		writer.writerow([SRC_CD,row[0],row[1],row[2],row[3],row[4],row[5],row[6],""])

	stdFile.close()
	outFile.close()

# Append records to TMPL_PRCS_CFG
# All records are generally the same, in the format: SUB_CD, 'N', '600'
# @param prcsCfgDataFile - Path of seedfile to be appended
def add_prcs_cfg_data(prcsCfgDataFile):
	f = open(prcsCfgDataFile, 'a')
	writer = csv.writer(f,quoting=csv.QUOTE_NONE,lineterminator=os.linesep)
	writer.writerow([SRC_CD,'N','600'])	

# # Append records to TMPL_OBJ_PRCS_EXCPN
# # @param objPrcsExcpnFile - Path of seedfile to be appended
# # @param standardsFile - Path of file to be read from (used as data input)
# def add_obj_prcs_excpn_data(objPrcsExcpnFile, standardsFile):


# # Append records to TMPL_OBJ_PRCS_EXCPN
# # @param objPrcsExcpnFile - Path of seedfile to be appended
# # @param standardsFile - Path of file to be read from (used as data input)
# def add_cust_adapt_data(custAdaptFile, standardsFile):	

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
	sql_query="create table sub_bkp_"+origProcessDate_text+" as select * from sub;create table nat_key_typ_bkp_"+origProcessDate_text+" as select * from nat_key_typ;create table dim_bkp_"+origProcessDate_text+" as select * from dim;create table sub_dim_nat_key_typ_"+origProcessDate_text+" as select * from sub_dim_nat_key_typ;"

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

# Send GKA-files from TempProcessing/ to default storage folder. Delete TempProcessing/ after successful push.
# Files are accessed by cka_config_data_load.ksh here for formulation of SQL Insert queries.
# Throws exception if ODS seedfiles are being pushed to the wrong directory.
# Throws exception if GKA seedfiles are being pushed to the wrong directory.
# @param seedfileType- Option specifying which seedfiles to push ("GKA" or "ODS")
def pushSeedData(seedfileType=None):

	# Also ensures that the actual modified seed-files are being pushed.
	if (seedfileType==None):
		print "No seedfiles were specified."
	elif (seedfileType=="GKA"):
		for row in gkaFiles:
			if (row.endswith(newProcessDate+".csv")):
				subprocess.call(["mv",row,GKA_INPUT_DEST])
		subprocess.call(['rm', '-r', 'TempProcessing'])
	elif (seedfileType=="ODS"):
		for row in odsFiles:
			if (row.endswith(newProcessDate+".csv")):
				subprocess.call(["mv",row,ODS_INPUT_DEST])
		subprocess.call(['rm', '-r', 'TempProcessing'])

# Backs up logfiles (e.g. datetimelog, datasrc.txt).
# Should be called before any modifications are made to the log-files (somewhere during start-up)
# Prerequisite: Time variables must be set. Original logfiles must be in place.
# Post: Backup files w/ timestamps in name created in logfile-specific BKP folder.
# Throws IOException if one or more original logfiles were not found.
# @param backup_dir - High-level dir in which to store backups (defaults to os.getcwd()/Resources/)
def backupLogfiles(backup_dir=os.path.join(os.getcwd(),"Resources")):
	
	if os.path.exists(datelogPath) and os.path.exists(subIdResourcePath):
		global datelogPath_backup, subIdResourcePath_backup
		backup_dir=os.path.join(backup_dir,"LogFiles_BKP_"+origProcessDate_text)
		if (os.path.exists(backup_dir)):
			shutil.rmtree(backup_dir)
		os.makedirs(backup_dir)

		# Define locations of backup logfiles
		datelogPath_backup=os.path.join(backup_dir,datelogPath.split('/')[-1])
		subIdResourcePath_backup=os.path.join(backup_dir,subIdResourcePath.split('/')[-1])

		# Create backups using shutil.copy2(src,dst)
		shutil.copy2(datelogPath,datelogPath_backup)
		shutil.copy2(subIdResourcePath,subIdResourcePath_backup)

# Resets environment to pre-processing state.
# Original backed-up seedfiles are sent back to GKA_INPUT_DEST. Backup folder is removed. New logfiles are removed.
# Original backed-up logfiles are sent back to Resources/. Backup folder is removed.
# TempProcessing/ and all sub-contents are removed.
def resetOriginalState():

	# Find and restore original seedfiles
	hasOrigSeedfile = True
	# Iterate through original locations tuple to determine whether 
	# original seedfiles are / aren't in backup folder.
	# Remove any new seedfiles that were pushed into directory.
	for f in odSeedfileLocations:
		if not os.path.exists(f):
			hasOrigSeedfile = False
		fNew = f.replace(origProcessDate,newProcessDate)
		if os.path.exists(fNew):
			os.remove(fNew)

	backupDir = os.path.join(ODS_INPUT_DEST,origProcessDate+"_BKP")
	if not hasOrigSeedfile:
		# Transfer only if backup folder exists. Otherwise raise an exception.
		if os.path.exists(backupDir):
			try:
				# Iterate through odsSeedfileLocations to get names and transfer back to GKA_INPUT_DEST
				for i in odSeedfileLocations:
					f = i.split('/')[-1]	# Get filename only
					f = os.path.join(backupDir,f)
					shutil.copy2(f,ODS_INPUT_DEST)
			except shutil.Error, msg:
				print "ERROR: " + msg
		else:
			raise IOException("resetOriginalState()\nERROR: Unable to find seedfile backup directory.")

	print "Datelog BKP: " + datelogPath_backup
	print "Sublog BKP: " + subIdResourcePath_backup

	# Find and restore original log-files
	# Only execute if backup files exist
	if os.path.exists(datelogPath_backup) and os.path.exists(subIdResourcePath_backup):
		print "ENTER LOG-FILE CONDITIONAL."

		# Remove working logfiles.
		os.remove(datelogPath)
		os.remove(subIdResourcePath)

		# Copy originals to ./Resources/
		shutil.copy2(datelogPath_backup,datelogPath)
		shutil.copy2(subIdResourcePath_backup,subIdResourcePath)

		# Remove backup directory + contents
		# shutil.rmtree(os.path.join(os.getcwd(),"Resources","LogFiles_BKP_"+origProcessDate_text))

	# Remove TempProcessing directory if exists
	tempPath = os.path.join(os.getcwd(),"TempProcessing")
	if os.path.exists(tempPath):
		shutil.rmtree(tempPath)


# Unarchive seedfiles of given processDate from backup folder in data/inputs/config (ODS_INPUT_DEST).
# Prerequisites: Backup folder with given processDate exists.
# Post-requisite: All seedfiles from backup folder are pushed into data/inputs/config. Backup folder is deleted.
# @param processDate - Date in (YYYYMMDD) which matches suffix of relevant seedfiles.
def revertSeedData(processDate):
	path = os.path.join(ODS_INPUT_DEST,processDate+'_BKP')
	if os.path.isdir(path):
		# Copy from src -> dest (backup folder --> ODS_INPUT_DEST)
		files = os.listdir(path)
		for f in files:
			if f.endswith(processDate+".csv"):
				try:
					shutil.copy(os.path.join(path,f), ODS_INPUT_DEST)	# Move from back-up folder (path) --> data/inputs/config/
				except IOError, msg:
					print IOError
					print msg
	else:
		raise IOError(path + " not found!")

# returns a tuple specifying values for:
# NTZ_ODS_STG_SVR
# NTZ_ODS_STG_UID
# NTZ_ODS_STG_DB
# NTZ_ODS_STG_PW
# NTZ_ODS_ODS_DB
# NTZ_ODS_CKR_DB
# @return 6-fold tuple containing the above information.
def inputConnectionDetails():
	global inputDataDict
	connectDetails = (inputDataDict["NTZ_ODS_STG_SVR"], inputDataDict["NTZ_ODS_STG_UID"], inputDataDict["NTZ_ODS_STG_DB"], inputDataDict["NTZ_ODS_STG_PW"], inputDataDict["NTZ_ODS_ODS_DB"], inputDataDict["NTZ_ODS_CKR_DB"])
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

	# Load previous and current processing dates
	loadDates(datelogPath)

	# Perform house-cleaning activities needed for startup
	# Establishes values for necessary input parameters
	initStartup()

	paramList = (newProcessDate_text, SRC_CD, SRC_DSC, SRC_ID, CKA_SRC_CD, CKA_SRC_ID, CLNT_CD, CLNT_DSC, CLNT_ID)
	connectParams = inputConnectionDetails()

	# Generate SQL command to run CIF_Config_Parameterized.sql,
	# complete with needed parameters.
	cmd = [od_connectionParam, "@CIF_Config_Parameterized.sql"]
	cmd += paramList
	cmd += connectParams
	cmd += (platformID, connectionID)

	# Generate SQL command to run Drop&Recreate tables script (CIF_Seedfile_Config_load.sql)
	dropRecreateParams = [od_connectionParam, "@"+dropRecreateTablesScript]

	# Query user whether they want to add or drop data (based on given PLATFORM ID)
	addOrDrop = raw_input("Add data (Y) or Drop data (N)? --> ")

	# If adding data: backup original seed-files, append to new seed-files,
	# 	> push new seed-files into data/inputs/config/, run SQL scripts, and
	# 	> run tlog_config_data_load.ksh script to write to ODconfig tables
	#	> update most recent processing date
	# Else if dropping data:
	#	> Run the data-removing SQL script.
	#	> Update most recent processing date (remove the last entered record)
	if (addOrDrop.upper() == "Y"):
		# Generate new seed-files
		copyOrigSeedfiles()

		# Backup original seed-files
		backupSeedFiles(ODS_INPUT_DEST, origProcessDate)

		# Backup original logfiles
		try:
			backupLogfiles()
		except IOError, msg:
			print msg
			resetOriginalState()
			sys.exit(1)

		# Add new records into seed-files
		add_obj_grp_data(odsFiles[2],objGrpStandardsFile)
		add_obj_data(odsFiles[1], objStdFile)
		add_sbj_area_data(odsFiles[5],sbjAreaStandardsFile)
		add_prcs_cfg_data(odsFiles[4])

		# Push seedfiles into data/inputs/config/
		# Only works in dev-environment
		pushSeedData("ODS")

		# Run SQL query to drop/recreate tables
		runSqlQuery(dropRecreateParams)
		
		# Run SQL query to backup ODconfig tables and load data into config tables
		runSqlQuery(cmd)

		# Run shell-script which appends seedfile data into ODconfig tables
		subprocess.call([odsDataLoad_script,newProcessDate])

		# Update datelogfile with most recent processing date
		updateDates(datelogPath, True)

		# Update datasrc.txt with newly added SUB_ID
		try:
			updateOrderFormInfo(subIdResourcePath)
		except IOError, msg:
			print "IOERROR: " + msg

	elif (addOrDrop.upper() == "N"):
		cmd[1] = "@removeAddendums.sql"
		updateDates(datelogPath, False)	# Remove previously entered processing date
		loadDates(datelogPath)			# Reload global date variables to reflect changes to datelog.csv
		
		# Push original seed-files (stored in backup folder under data/inputs/config/) into the working dir.
		# This is needed to ensure that next run of script will have available seedfiles to write to.
		try:
			revertSeedData(origProcessDate)
		except IOError, msg:
			print msg

		runSqlQuery(cmd)

if __name__ == '__main__':
	main()