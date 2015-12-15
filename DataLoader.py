#!/usr/local/bin/python2.4

import os, sys, stat
import errno, shutil
import subprocess
import csv

from collections import deque
from subprocess import Popen, PIPE
from datetime import datetime, date, time

pre_gka=os.getcwd()+"/GKA/"
suffix=".csv"

# Standards files (.csv's enlisting default/required data for each seed-file)
objGrpStandardsFile = os.getcwd()+"/Resources/OBJ_GRP_STANDARD.csv"
sbjAreaStandardsFile = os.getcwd()+"/Resources/SBJ_AREA_STANDARD.csv"
natKeyStandardsFile = os.getcwd()+"/Resources/NAT_KEY_STANDARD.csv"
subDimNatStandardsFile = os.getcwd()+"/Resources/SUB_DIM_NAT_STANDARD.csv"
natKeyStandardsFile_SCD = os.getcwd()+"/Resources/NAT_KEY_SCD_STANDARD.csv"

# Temporary standards files (needed to modify data values for each new run)
temp_natKeyStandardsFile = ''
temp_subDimNatStandardsFile = ''

# Login information for databases and environments
# To-Do: ROUTE PASSWORD INPUT THROUGH ODconfig
userGKA="AODR45CKAADVD"
passwordGKA="ckaadvaodr5dev"
sidGKA="CKA280D"
connectionString=userGKA+"/"+passwordGKA+"@"+sidGKA

# Command to initiate and connect to SQL*PLUS
# sqlplus -S AODR45CKAADVD/ckaadvaodr5dev@CKA280D
# End login information

# Table information for GKA
subTable="SUB_LOYALTYTEST"
subDimNatKeyTable="SUB_DIM_NAT_KEY_TYP_LOYALTYTEST"

# seed-file info (TEMPORARY)
subSeedName="TMPL_SUB_DATA_20150914.csv"

# Other parameters
geolocation = "US"		# USA is default value

# DIRECTORY VARIABLES
CKA_CODEBASE_KSH="/dsd_2/relr45d/ckaadv/code/bin/"
CKA_CODEBASE_PYTHON="/dsd_2/relr45d/ckaadv/code/python/"
GKA_INPUT_DEST="/dsd_2/relr45d/ckaadv/data/inputs/config/"

# Shell-scripts
ckaDataLoad_script=CKA_CODEBASE_KSH+"cka_config_data_load.ksh"

# Standard Nat_Key_IDs | Loaded in initStartup()
standardNatKeyDict = {}

gkaSeedfileLocations = []
gkaFiles = ()

# ********Variables added THURSDAY 12-10-15*********** #
# Input parameters (will be loaded from OrderForm.csv)
SRC_DSC = ''
SRC_CD = ''
SRC_ID = -1
Geolocation = ''
prodNatKeyID = -1
hasPromo = ''
hasPromoDetail = ''

# INPUT FILE (from order-form)
inputFileName = "OrderForm.csv"
inputFilePath = ""
inputDataDict = {}	# Dictionary containing all input vars.

# Log-file paths
datelogPath=os.path.join(os.getcwd(),'Resources/datetimelog.csv')
subIdResourcePath=os.path.join(os.getcwd(),'Resources/datasrc.txt')
prodNatKeyResourcePath=os.path.join(os.getcwd(),'Resources/datasrc2.txt')
datelogPath_backup=''
subIdResourcePath_backup=''
prodNatKeyResourcePath_backup=''

# Processing date vars
origProcessDateObj=''	
origProcessDate=''		# E.g. "20150914"
origProcessDate_text=''	# E.g. "11sep2015"
newProcessDateObj=''
newProcessDate=''
newProcessDate_text=''
# ********END Variables added THURSDAY 12-10-15*********** #

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

			
			# print "KEY: " + key + "\tVALUE: " + val
			# print type(val)
			# DATA VALIDATION
			headStr = "ORDER-FORM ERROR: "
			if key == "PRODUCT NAT-KEY":
				if type(val) is str:
					val = val.upper()
					# Convert to Python integer if isdigit
					if val.isdigit():
						val = int(val)
					elif not val == "NEW":
						raise ValueError(headStr+"\'PRODUCT NAT-KEY\' must be \'NEW\' or a valid integer.")
			elif key == "PROMO?":
				val = val.upper()
				if not (val == 'Y' or val == 'N'):
					raise ValueError(headStr+"\'PROMO\' must be either \'Y\' or \'N\'.")
				elif val == 'Y':
					val = True
				elif val == 'N':
					val = False
			elif key == "PROMODETAIL?":
				val = val.upper()
				if not (val == 'Y' or val == 'N'):
					raise ValueError(headStr+"\'PROMODETAIL\' must be either \'Y\' or \'N\'.")
				elif val == 'Y':
					val = True
				elif val == 'N':
					val = False

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

# Set all items needed for startup/initialization
# loadInputData() - Load input data (from order-form) into dictionary inputDataDict.
# Load values in inputDataDict into global variables (e.g. SRC_CD).
# Copy most recent seedfiles from data/input/config/ into working directory
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
		print key + ": " + str(value)

	# Establish variable names from dictionary
	# Ensure that values are assigned to the global variables
	global SRC_DSC, SRC_CD, SRC_ID, Geolocation, prodNatKeyID, hasPromo, hasPromoDetail
	SRC_DSC = inputDataDict["Subscriber Name"]
	SRC_CD = inputDataDict["Subscriber Code"]
	SRC_ID = inputDataDict["Subscriber ID"]
	Geolocation = inputDataDict["Geolocation"]
	prodNatKeyID = inputDataDict["PRODUCT NAT-KEY"]
	hasPromo = inputDataDict["PROMO?"]
	hasPromoDetail = inputDataDict["PROMODETAIL?"]

	# Temporary standards files (needed to modify data values for each new run)
	global temp_natKeyStandardsFile, temp_subDimNatStandardsFile
	temp_natKeyStandardsFile = os.path.join(os.getcwd(),"TempProcessing","NAT_KEY_STANDARD_"+newProcessDate+".csv")
	temp_subDimNatStandardsFile = os.path.join(os.getcwd(),"TempProcessing","SUB_DIM_NAT_STANDARD_"+newProcessDate+".csv")
	
	# Establish original locations of original ODS seed-files
	global gkaSeedfileLocations
	gkaSeedfileLocations = [GKA_INPUT_DEST + "TMPL_DIM_DATA_" + origProcessDate + suffix,
						GKA_INPUT_DEST + "TMPL_NAT_KEY_TYP_DATA_" + origProcessDate + suffix,
						GKA_INPUT_DEST + "TMPL_SUB_DATA_" + origProcessDate + suffix,
						GKA_INPUT_DEST + "TMPL_SUB_DIM_NAT_KEY_TYP_DATA_" + origProcessDate + suffix]

	# Load nat-key dictionary
	global standardNatKeyDict
	standardNatKeyDict = {
		"PRODUCT_LEGACY":2,
		"PROD_US":40,
		"PRODUCT_SCD":47,
		"PROD_EU":73,
		"PROMODETAIL_LOY":68,
		"PROMOTION_LOY":69,
		"PERIOD_SECOND":3,
		"PERIOD_DAY":10,
		"PERIOD_WEEK":11,
		"PERIOD_DAY_PART":12,
		"PERIOD_DAY_PART_SCD":14,
		"PERIOD_SECOND_GLOBAL":36,
		"PERIOD_DAY_PART_HR":39,
		"PERIOD_DAY_NEW":44,
		"PERIOD_WEEK_NEW":45,
		"PERIOD_DAY_PART_NEW":46,
		"PERIOD_DAY_PART_SCD_NEW":48
	}						

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

# Copies seedfiles with appropriate processing dates from data/inputs/config/
# into temporary working directory.
def copyOrigSeedfiles():

	# Create TemporaryProcessing directory to hold seedfiles
	path=os.path.join(os.getcwd(),"TempProcessing")
	if not os.path.exists(path):
		os.makedirs(path)

	# Generate temporary duplicates of standards-files
	shutil.copy2(natKeyStandardsFile, temp_natKeyStandardsFile)
	shutil.copy2(subDimNatStandardsFile, temp_subDimNatStandardsFile)

	global gkaFiles
	gkaFiles = list()

	# Copy new version (w/ updated process date) of seed-file to the new path
	# Throw errors if all specified seed-files don't exist in source directory
	# or if source == destination. 
	for seedfile in gkaSeedfileLocations:
		seedfileName=seedfile.split('/')[-1]

		# Modify name to describe new processing date
		seedfileName = seedfileName.replace(origProcessDate, newProcessDate)
		
		try:
			shutil.copy2(seedfile, os.path.join(path,seedfileName))
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

		gkaFiles.append(os.path.join(path,seedfileName))
	print gkaFiles

	# # Generate temporary duplicates of standards-files
	# shutil.copy2(natKeyStandardsFile, temp_natKeyStandardsFile)
	# shutil.copy2(subDimNatStandardsFile, temp_subDimNatStandardsFile)

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

# Append record to TMPL_SUB_DATA_20150914.csv (in gkaFiles[2])
def add_sub_data(subscriberDataFile):
	# Parameter 'a' signifies to writer that it should append to file
	f = open(subscriberDataFile, 'a')
	csvWriter = csv.writer(f, quoting=csv.QUOTE_ALL)
	csvWriter.writerow([SRC_ID,SRC_CD,SRC_DSC])
	f.close()

# Appends to corresponding seed-file.
# NOTE: Does not create new NATURAL KEY TYPES (identifiers for dimensions)
def add_sub_dim_nat_data(subDimNatDataFile, standardsFile):

	stdFile = open(standardsFile)			# read-only
	outFile = open(subDimNatDataFile, 'a')	# write-file (being appended)

	reader = csv.reader(stdFile)
	writer = csv.writer(outFile,quoting=csv.QUOTE_NONE,lineterminator='\n')

	# What is NAT_KEY_ID going to be (new product is created)

	for row in reader:
		writer.writerow([SRC_CD,row[1],row[2],"Y","N"])

# Adds default natural key types (Store, Basket, Household, ID_CARD)
# @param natKeyDataFile - Seed-file containing Natural Key Type data 
# @param standardsFile - Standards File which contains default entry values for seed-file specified by natKeyDataFile
# Return Last NAT_KEY_TYP_ID + 1 (from original file; before adding new records). Specifies starting point for new ID creation.
def add_default_nat_key_data(natKeyDataFile, standardsFile):

	stdFile = open(standardsFile,'rb')
	outFile = open(natKeyDataFile, 'a')

	reader = csv.reader(stdFile,delimiter=',')
	writer = csv.writer(outFile,quoting=csv.QUOTE_NONE,escapechar='\n',lineterminator='\n')

	startID = int(get_last_row(natKeyDataFile)[0]) + 1
	currentID = startID

	global SRC_CD, SRC_DSC

	for row in reader:

		tempRow = row
		# Assign and process field values
		tempRow[0] = row[0].replace("***",SRC_CD.upper())
		tempRow[1] = row[1].replace("***",SRC_DSC.upper())
		tempRow[4] = row[4].replace("***",SRC_DSC.title())

		# Add new NAT_KEY_ID to first field
		tempRow.insert(0,currentID)

		writer.writerow(tempRow)
		currentID = currentID + 1

	stdFile.close()
	outFile.close()

	return startID

# Update the standards file used to complete TMPL_SUB_DIM_NAT_... 
# Specifically, updates the NAT_ID values for newly created natural key records in TMPL_NAT_DATA
# Default value for Product NAT_KEY has been set to 40 (representing a US client).
def update_sub_dim_nat_standards(standardsFile, start_NAT_ID, product_NAT_ID=40):

	stdFile = open(standardsFile,'rU')

	tmpFile = os.getcwd()+"/Resources/TempFile.csv"
	outFile = open(os.getcwd()+"/Resources/TempFile.csv",'wb')

	reader = csv.reader(stdFile,delimiter=',')
	writer = csv.writer(outFile,quoting=csv.QUOTE_NONE,escapechar='\n',lineterminator='\n')

	current_id = start_NAT_ID

	for row in reader:
		if row[0] == "PROMOTION":
			writer.writerow([row[0],row[1],standardNatKeyDict["PROMOTION_LOY"],row[3],row[4]])
		elif row[0] == "PROMODETAIL":
			writer.writerow([row[0],row[1],standardNatKeyDict["PROMODETAIL_LOY"],row[3],row[4]])
		elif row[0] == "PRODUCT":
			writer.writerow([row[0],row[1],product_NAT_ID,row[3],row[4]])
		elif row[0] == "PERIOD":
			writer.writerow([row[0],row[1],standardNatKeyDict["PERIOD_SECOND_GLOBAL"],row[3],row[4]])	
		elif row[2] == "VARIABLE":
			writer.writerow([row[0],row[1],current_id,row[3],row[4]])
			current_id += 1

	stdFile.close()
	outFile.close()

	shutil.copy2(tmpFile, standardsFile)
	os.remove(tmpFile)

# Adds default dimension and nat-key values to TMPL_SUB_DIM_NAT_KEY_TYP_DATA
# (PROD, PER, STORE, BAS, HHOLD, ID_CARD)
# Record Format: SRC_ID | DIM_ID | NAT_KEY_ID | Y | N
# @param subDimNatDataFile - TMPL_SUB_DIM_NAT_DATA seedfile, to which new records are appended.
# @param standardsFile - Default values for each record being added (used as template for new records).
# @param prodNatKey - Int value of user-specified Product Natural Key (must be spec'd if not creating
#	a new key).
# @param geolocation - Geographic region of client. Was used to determine Product Nat-Key; currently not in use.
def add_default_sub_dim_nat_data(subDimNatDataFile, standardsFile, prodNatKey, geolocation=None):

	stdFile = open(standardsFile, 'rb')
	outFile = open(subDimNatDataFile, 'a')

	reader = csv.reader(stdFile,delimiter=',')
	writer = csv.writer(outFile,quoting=csv.QUOTE_NONE,escapechar='\n',lineterminator='\n')

	# PRODUCT and PERIOD have default values (passed as parameters)
	# Add records to SUB_DIM_NAT_KEY_TYP_DATA based on standards file
	for row in reader:
		if row[0] == "PRODUCT":
			# if geolocation == "EU":
			# 	writer.writerow([SRC_ID,row[1],standardNatKeyDict["PROD_EU"],row[3],row[4]])
			# elif geolocation == "US":
			# 	writer.writerow([SRC_ID,row[1],standardNatKeyDict["PROD_US"],row[3],row[4]])
			# elif (geolocation == None and prodNatKey != None):
			# 	writer.writerow([SRC_ID,row[1],prodNatKey,row[3],row[4]])
			# else:
			# 	# THROW EXCEPTION HERE
			# 	print "ERROR:\t\tadd_default_sub_dim_nat_data()\t\tneed geolocation OR prodNatKey"
			writer.writerow([SRC_ID,row[1],prodNatKey,row[3],row[4]])
		elif row[0] == "PERIOD":
			writer.writerow([SRC_ID,row[1],standardNatKeyDict["PERIOD_SECOND_GLOBAL"],row[3],row[4]])
		elif row[0] != "PROMOTION" and row[0] != "PROMODETAIL":
			writer.writerow([SRC_ID,row[1],row[2],row[3],row[4]])

	stdFile.close()
	outFile.close()

# Adds specified optional dimension(s) to TMPL_SUB_DIM_NAT_KEY_TYP_DATA.csv (either PROMOTION or PROMODETAIL or both)
# NOTE: This function should be called only if one of promo or promodetail are True.
# @param promo Boolean specifying whether PROMO dimension should be added. Y = add | N = don't add
# @param promodetail Boolean specifying whether PROMODETAIL dimension should be added.
# @param subDimNataDataFile String containing location of seedfile TMPL_SUB_DIM_NAT_KEY_DATA.csv
# @param subDimNatStandardsFile String containing location of standards file SUB_DIM_NAT_STANDARDS.csv
def add_opt_dimensions(promo, promodetail, subDimNatDataFile, subDimNatStandardsFile):
	
	stdFile = open(subDimNatStandardsFile, 'rb')
	outFile = open(subDimNatDataFile, 'a')

	reader = csv.reader(stdFile,delimiter=',')
	writer = csv.writer(outFile,quoting=csv.QUOTE_NONE,escapechar='\n',lineterminator='\n')

	if promo and promodetail:
		for row in reader:
			if (row[0] == "PROMOTION" or row[0] == "PROMODETAIL"):
				writer.writerow([SRC_ID,row[1],row[2],row[3],row[4]])
	elif promo:
		for row in reader:
			if (row[0] == "PROMOTION"):
				writer.writerow([SRC_ID,row[1],row[2],row[3],row[4]])
	elif promodetail:
		for row in reader:
			if (row[0] == "PROMODETAIL"):
				writer.writerow([SRC_ID,row[1],row[2],row[3],row[4]])

	stdFile.close()
	outFile.close()

## Create new PRODUCT_GLOBAL_SCD Key. Used only when specified by user.
# @param natKeyDataFile Points to TMPL_NAT_KEY_DATA seedfile, adds new PRODUCT_GLOBAL_SCD here
# @param standardsFile Contains PRODUCT_GLOBAL_SCD key data (points to NAT_KEY_STANDARDS_PRODUCT.csv)
# @param new_nat_id Integer value of new Natural Key ID to be assigned to the new PRODUCT nat-key.
def update_product_nat_key(natKeyDataFile, standardsFile, new_nat_id):

	stdFile = open(standardsFile, 'rb')
	outFile = open(natKeyDataFile, 'a')

	reader = csv.reader(stdFile,delimiter=',')
	writer = csv.writer(outFile,quoting=csv.QUOTE_NONE,escapechar='\n',lineterminator='\n')

	for row in reader:
		tempList = [new_nat_id]
		tempList.extend(row[1:-1])
		writer.writerow(tempList)

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
	sql_query="create table sub_bkp_"+origProcessDate_text+" as select * from sub;create table nat_key_typ_bkp_"+origProcessDate_text+" as select * from nat_key_typ;create table dim_bkp_"+origProcessDate_text+" as select * from dim;create table sub_dim_nat_key_typ_"+origProcessDate_text+" as select * from sub_dim_nat_key_typ;"

# Generate SQL file for GKA database
# @param tableName
# @param seed-file
# return SQL query
def createGkaQuery(tableName, seedFile):

	# Call helper method
	queryResult = getColNames(tableName)
	headerList = queryResult.split('\n')
	headerList.pop()	# Remove last entry (empty)
	print headerList
	print "\n\n\n*****************************\n"
	print queryResult

	# Logic for generating SQL script (need seed-file)
	# 1) Open file
	# 2) Parse through each record (except first record --> contains headers)
	# 3) For-each record: generate SQL script
	
	file = open(seedFile, 'rb')
	reader = csv.reader(file)

	seedfileHeader = reader.next()		# skip header row and get number of fields in record
	recordLength = len(seedfileHeader)
	headerDiff = len(headerList) - recordLength

	# Align seed-file fields with actual columns from table (stored in headerList)
	# In many cases, the seed-file does not contain all required fields, and thus
	# doesn't match up 1:1 with the CKA DB table columns (usually the missing fields are null)
	if headerDiff > 0:
		for i in range(0, headerDiff, 1):
			headerList.pop()

	sqlInsert = ("INSERT INTO "+tableName+" ("+', '.join(['%s']*len(headerList))+")") % tuple(headerList)
	sqlVals = "VALUES "

	fullSqlQuery = ""

	for row in reader:
		sqlVals += ("("+', '.join(['\'%s\'']*len(row))+");") % tuple(row)
		fullSqlQuery += sqlInsert + "\n" + sqlVals + "\n\n"
		sqlVals = "VALUES "	# RESET string

	return fullSqlQuery	

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

# Function that takes the sqlCommand and connectString and returns the queryResult and errorMessage (if any)
# CREDIT: https://moizmuhammad.wordpress.com/2012/01/31/run-oracle-commands-from-python-via-sql-plus/
def runSqlQuery(sqlCommand, connectString):
   session = Popen(['sqlplus', '-S', connectString], stdin=PIPE, stdout=PIPE, stderr=PIPE)
   session.stdin.write(sqlCommand)
   return session.communicate()

# Send GKA-files from TempProcessing/ to default storage folder.
# Files are accessed by cka_config_data_load.ksh here for formulation of SQL Insert queries.
# Throws exception if ODS seedfiles are being pushed to the wrong directory.
# Throws exception if GKA seedfiles are being pushed to the wrong directory.
# @param seedfileType- Option specifying which seedfiles to push ("GKA" or "ODS")
def pushSeedData(seedfileType=None):

	# if (seedfileType==None):
	# 	print "No seedfiles were specified."
	# elif (seedfileType=="GKA"):
	# 	for row in gkaFiles:
	# 		subprocess.call(["mv",row,GKA_INPUT_DEST])
	# elif (seedfileType=="ODS"):
	# 	for row in 	odsFiles:
	# 		subprocess.call(["mv",row,ODS_INPUT_DEST])

	# Also ensures that the actual modified seed-files (with new process-date) are being pushed.
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
	
	if os.path.exists(datelogPath) and os.path.exists(subIdResourcePath) and os.path.exists(prodNatKeyResourcePath):
		global datelogPath_backup, subIdResourcePath_backup, prodNatKeyResourcePath_backup
		backup_dir=os.path.join(backup_dir,"LogFiles_BKP_"+origProcessDate_text)
		if (os.path.exists(backup_dir)):
			shutil.rmtree(backup_dir)
		os.makedirs(backup_dir)

		# Define locations of backup logfiles
		datelogPath_backup=os.path.join(backup_dir,datelogPath.split('/')[-1])
		subIdResourcePath_backup=os.path.join(backup_dir,subIdResourcePath.split('/')[-1])
		prodNatKeyResourcePath_backup=os.path.join(backup_dir,prodNatKeyResourcePath.split('/')[-1])

		# Create backups using shutil.copy2(src,dst)
		shutil.copy2(datelogPath,datelogPath_backup)
		shutil.copy2(subIdResourcePath,subIdResourcePath_backup)
		shutil.copy2(prodNatKeyResourcePath,prodNatKeyResourcePath_backup)
	else:
		raise IOError("IOERROR: One or more of the logfiles were not found in ./Resources/")

# Resets environment to pre-processing state.
# Original backed-up seedfiles are sent back to GKA_INPUT_DEST. Backup folder is removed. New logfiles are removed.
# Original backed-up logfiles are sent back to Resources/. Backup folder is removed.
# TempProcessing/ and all sub-contents are removed.
def resetOriginalState():

	# Find and restore original seedfiles
	hasOrigSeedfile = True
	# Iterate through original locations tuple to determine whether 
	# original seedfiles are / aren't in backup folder.
	for f in gkaSeedfileLocations:
		if not os.path.exists(f):
			hasOrigSeedfile = False

	backupDir = os.path.join(GKA_INPUT_DEST,origProcessDate+"_BKP")
	if not hasOrigSeedfile:
		# Transfer only if backup folder exists. Otherwise raise an exception.
		if os.path.exists(backupDir):
			try:
				# Iterate through gkaSeedfileLocations to get names and transfer back to GKA_INPUT_DEST
				for i in gkaSeedfileLocations:
					f = i.split('/')[-1]	# Get filename only
					f = os.path.join(backupDir,f)
					shutil.move(f,GKA_INPUT_DEST)
			except shutil.Error, msg:
				print "ERROR: " + msg
		else:
			raise IOException("resetOriginalState()\nERROR: Unable to find seedfile backup directory.")

	# Find and restore original log-files
	# Only execute if backup files exist
	if os.path.exists(datelogPath_backup) and os.path.exists(subIdResourcePath_backup) and os.path.exists(prodNatKeyResourcePath_backup):
		# Remove working logfiles.
		os.remove(datelogPath)
		os.remove(subIdResourcePath)
		os.remove(prodNatKeyResourcePath)

		# Copy originals to ./Resources/
		shutil.copy2(datelogPath_backup,datelogPath)
		shutil.copy2(subIdResourcePath_backup,subIdResourcePath)
		shutil.copy2(prodNatKeyResourcePath_backup,prodNatKeyResourcePath)

		# Remove backup directory + contents
		# shutil.rmtree(os.path.join(os.getcwd(),"Resources","LogFiles_BKP_"+origProcessDate_text))

	# Remove TempProcessing directory if exists
	tempPath = os.path.join(os.getcwd(),"TempProcessing")
	if os.path.exists(tempPath):
		shutil.rmtree(tempPath)

# Update product natural key information in appropriate logfile.
# @param prodNatLogfile - Location of logfile containing used product natural key information.
# @param prodNatKeyID - Product Nat-Key ID of current client
# @param isNewID - Boolean stating whether Nat-Key ID is new. If new, appends a new record to logfile.
def updateProdNatInfo(prodNatLogfile, prodNatKeyID, isNewID=False):
	if os.path.exists(prodNatLogfile):
		if isNewID:
			f = open(prodNatLogfile, 'a')
			writer = csv.writer(f,quoting=csv.QUOTE_NONE,lineterminator=os.linesep)
			writer.writerow([prodNatKeyID,SRC_CD])
		else:
			readFile = open(prodNatLogfile, 'rb')
			writeFile = open("temp_prodNat", 'a')	# Generates new temp file

			reader = csv.reader(readFile,delimiter=',')
			writer = csv.writer(writeFile,quoting=csv.QUOTE_NONE,lineterminator=os.linesep)

			# Write contents of original logfile to temp logfile.
			# Make transformation where necessary.
			for row in reader:
				# If record contains same PROD NAT-KEY ID as current client, 
				# add current client code to record.
				if row[0] == prodNatKeyID:
					row.append(SRC_CD)
				writer.writerow(row)

			# Close open files
			readFile.close()
			writeFile.close()

			# Copy temp file back to original. Remove temp file.
			shutil.copy2("temp_prodNat",prodNatLogfile)
			os.remove("temp_prodNat",prodNatLogfile)
	else:
		raise IOError("Unable to find " + prodNatLogfile)

# MAIN SCRIPT
# Currently able to write out standard/default values for SUBSCRIBER, OBJECT_GROUPS, and SUBJECT_AREAS
# ADDENDUM 10/26/15: Also writing out default values for TMPL_NAT_KEY_DATA, TMPL_SUB_DIM_NAT_KEY_DATA
def main():

	# Load previous and current processing dates
	loadDates(datelogPath)

	# Perform house-cleaning activities needed for startup
	# Establishes values for necessary input parameters by calling loadInputData()
	initStartup()

	# Generate new working seed-files
	copyOrigSeedfiles()

	# Create backups of original seedfiles. Move to backup dir in data/inputs/config/
	backupSeedFiles(GKA_INPUT_DEST,origProcessDate)

	# Create backups of original logfiles. Move to backup dir in Resources/
	try:
		backupLogfiles()
	except IOError, msg:
		print msg
		resetOriginalState()
		sys.exit(1)

	productKeyBranch = False	# Default value
	# In case user has requested new PROD NAT_KEY creation
	if prodNatKeyID == "NEW":
		productKeyBranch = True

	# Append record(s) to TMPL_SUB_DATA
	add_sub_data(gkaFiles[2])

	# Modify temporary standards files to prepare entries for seed-files.	
	# If NO new Product / Period key created, use original Sub-Dim-Nat Standards File
	# Else, use newly created Standards File	
	natkeyID = add_default_nat_key_data(gkaFiles[1],natKeyStandardsFile)
	if (productKeyBranch):
		# Retrieve last used ID from TMPL_NAT_KEY and use to generate newest Nat_Key_ID
		newNatID = int(get_last_row(gkaFiles[1])[0]) + 1
		update_product_nat_key(gkaFiles[1],natKeyStandardsFile_SCD,newNatID)
		update_sub_dim_nat_standards(temp_subDimNatStandardsFile,natkeyID,newNatID)
		add_default_sub_dim_nat_data(gkaFiles[3],temp_subDimNatStandardsFile, prodNatKey=newNatID)
	else:
		newNatID = prodNatKeyID
		update_sub_dim_nat_standards(temp_subDimNatStandardsFile,natkeyID)
		# prodNatKeyId must be an integer if it's value wasn't 'NEW'
		add_default_sub_dim_nat_data(gkaFiles[3],temp_subDimNatStandardsFile,prodNatKeyID)

	# Add PROMO and/or PROMODETAIL dimensions if options were specified
	if hasPromo and hasPromoDetail:
		add_opt_dimensions(True,True,gkaFiles[3],temp_subDimNatStandardsFile)
	elif hasPromo:
		add_opt_dimensions(True,False,gkaFiles[3],temp_subDimNatStandardsFile)
	elif hasPromoDetail:
		add_opt_dimensions(False,True,gkaFiles[3],temp_subDimNatStandardsFile)

	# Update log-files (datetime, subscriber info, product nat-key)
	updateDates(datelogPath,True)
	updateOrderFormInfo(subIdResourcePath)
	updateProdNatInfo(prodNatKeyResourcePath, newNatID, productKeyBranch)

	# Move new seed-files into data/inputs/config/
	pushSeedData("GKA")

	# Trigger cka_config_data_load.ksh to output to CKA DB
	# subprocess.call([ckaDataLoad_script,newProcessDackte])

if __name__ == '__main__':
	main()
