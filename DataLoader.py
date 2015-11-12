#!/usr/local/bin/python2.4

import os, sys, stat
import errno, shutil
import subprocess
import csv

from collections import deque
from subprocess import Popen, PIPE

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
natKeyStandardsFile = os.getcwd()+"/Resources/NAT_KEY_STANDARD.csv"
subDimNatStandardsFile = os.getcwd()+"/Resources/SUB_DIM_NAT_STANDARD.csv"
natKeyStandardsFile_SCD = os.getcwd()+"/Resources/NAT_KEY_SCD_STANDARD.csv"

# Temporary standards files (needed to modify data values for each new run)
temp_natKeyStandardsFile = os.getcwd()+"/TempProcessing/NAT_KEY_STANDARD_"+newProcessDate+".csv"
temp_subDimNatStandardsFile = os.getcwd()+"/TempProcessing/SUB_DIM_NAT_STANDARD_"+newProcessDate+".csv"

# Login information for databases and environments
# To-Do: ROUTE PASSWORD INPUT THROUGH ODconfig
userGKA="AODR45CKAADVD"
passwordGKA="ckaadvaodr5dev"
sidGKA="CKA280D"
connectionString=userGKA+"/"+passwordGKA+"@"+sidGKA

userODS=""
passwordODS=""
sidODS=""
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

ODS_CODEBASE_KSH="/dsd_2/relr45d/tlog/code/bin/"
ODS_INPUT_DEST="/dsd_2/relr45d/tlog/data/inputs/config/"

# Shell-scripts
ckaDataLoad_script=CKA_CODEBASE_KSH+"cka_config_data_load.ksh"
odsDataLoad_script=ODS_CODEBASE_KSH+"tlog_config_data_load_v2.ksh"

# Standard Nat_Key_IDs
# Sourced directly from TMPL_NAT_KEY_TYP_DATA
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

gkaSeedfileLocations = [pre_gka + "TMPL_DIM_DATA_" + processDate + suffix,
						pre_gka + "TMPL_NAT_KEY_TYP_DATA_" + processDate + suffix,
						pre_gka + "TMPL_SUB_DATA_" + processDate + suffix,
						pre_gka + "TMPL_SUB_DIM_NAT_KEY_TYP_DATA_" + processDate + suffix]


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
gkaFiles = list()

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

for seedfile in gkaSeedfileLocations:
	seedfileName=seedfile.split('/')[-1]

	# Modify name to describe new processing date
	seedfileName = seedfileName.replace(processDate, newProcessDate)
	shutil.copy2(seedfile, path+seedfileName)

	# Unsafe programming practice to keep files open
	# gkaFiles.append(open(path+seedfileName))
	gkaFiles.append(path+seedfileName)

# Generate temporary duplicates of standards-files
shutil.copy2(natKeyStandardsFile, temp_natKeyStandardsFile)
shutil.copy2(subDimNatStandardsFile, temp_subDimNatStandardsFile)

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
	csvWriter.writerow([SUB_ID,SUB_NM,SUB_DSC])
	f.close()

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

# Appends to corresponding seed-file.
# NOTE: Does not create new NATURAL KEY TYPES (identifiers for dimensions)
def add_sub_dim_nat_data(subDimNatDataFile, standardsFile):

	stdFile = open(standardsFile)			# read-only
	outFile = open(subDimNatDataFile, 'a')	# write-file (being appended)

	reader = csv.reader(stdFile)
	writer = csv.writer(outFile,quoting=csv.QUOTE_NONE,lineterminator='\n')

	# What is NAT_KEY_ID going to be (new product is created)

	for row in reader:
		writer.writerow([SUB_NM,row[1],row[2],"Y","N"])

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

	for row in reader:

		tempRow = row
		# Assign and process field values
		tempRow[0] = row[0].replace("***",SUB_NM.upper())
		tempRow[1] = row[1].replace("***",SUB_DSC.upper())
		tempRow[4] = row[4].replace("***",SUB_DSC.title())

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
# Record Format: SUB_ID | DIM_ID | NAT_KEY_ID | Y | N
def add_default_sub_dim_nat_data(subDimNatDataFile, standardsFile, geolocation=None, prodNatKey=None):

	stdFile = open(standardsFile, 'rb')
	outFile = open(subDimNatDataFile, 'a')

	reader = csv.reader(stdFile,delimiter=',')
	writer = csv.writer(outFile,quoting=csv.QUOTE_NONE,escapechar='\n',lineterminator='\n')

	# PRODUCT and PERIOD have default values (passed as parameters)
	# Add records to SUB_DIM_NAT_KEY_TYP_DATA based on standards file
	for row in reader:
		if row[0] == "PRODUCT":
			if geolocation == "EU":
				writer.writerow([SUB_ID,row[1],standardNatKeyDict["PROD_EU"],row[3],row[4]])
			elif geolocation == "US":
				writer.writerow([SUB_ID,row[1],standardNatKeyDict["PROD_US"],row[3],row[4]])
			elif (geolocation == None and prodNatKey != None):
				writer.writerow([SUB_ID,row[1],prodNatKey,row[3],row[4]])
			else:
				# THROW EXCEPTION HERE
				print "ERROR:\t\tadd_default_sub_dim_nat_data()\t\tneed geolocation OR prodNatKey"
		elif row[0] == "PERIOD":
			writer.writerow([SUB_ID,row[1],standardNatKeyDict["PERIOD_SECOND_GLOBAL"],row[3],row[4]])
		elif row[0] != "PROMOTION" and row[0] != "PROMODETAIL":
			writer.writerow([SUB_ID,row[1],row[2],row[3],row[4]])

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
				writer.writerow([SUB_ID,row[1],row[2],row[3],row[4]])
	elif promo:
		for row in reader:
			if (row[0] == "PROMOTION"):
				writer.writerow([SUB_ID,row[1],row[2],row[3],row[4]])
	elif promodetail:
		for row in reader:
			if (row[0] == "PROMODETAIL"):
				writer.writerow([SUB_ID,row[1],row[2],row[3],row[4]])

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
	sql_query="create table sub_bkp_"+processDate_text+" as select * from sub;create table nat_key_typ_bkp_"+processDate_text+" as select * from nat_key_typ;create table dim_bkp_"+processDate_text+" as select * from dim;create table sub_dim_nat_key_typ_"+processDate_text+" as select * from sub_dim_nat_key_typ;"


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

	if (seedfileType==None):
		print "No seedfiles were specified."
	elif (seedfileType=="GKA"):
		for row in gkaFiles:
			subprocess.call(["mv",row,GKA_INPUT_DEST])
	elif (seedfileType=="ODS"):
		for row in 	odsFiles:
			subprocess.call(["mv",row,ODS_INPUT_DEST])


# MAIN SCRIPT
# Currently able to write out standard/default values for SUBSCRIBER, OBJECT_GROUPS, and SUBJECT_AREAS
# ADDENDUM 10/26/15: Also writing out default values for TMPL_NAT_KEY_DATA, TMPL_SUB_DIM_NAT_KEY_DATA
def main():

	add_sub_data(gkaFiles[2])
	add_obj_grp_data(odsFiles[2],objGrpStandardsFile)
	add_sbj_area_data(odsFiles[5],sbjAreaStandardsFile)

	# Prompt user if they want to create new PRODUCT_GLOBAL_SCD
	# If yes, generate/update new product NAT_KEY_TYP in:
	# TMPL_NAT_KEY_DATA, natKeyStandards, subDimNatStandards
	productKeyBranch = raw_input("Create new product key? (Y/N) >> ")

	# Prompt user for client geographical location (impacts NAT_KEY_ID of PROD dimension)
	geolocation = raw_input("Enter client geographical continent (\"EU\" or \"US\") >> ")
	
	# Modify temporary standards files to prepare entries for seed-files.	
	# If NO new Product / Period key created, use original Sub-Dim-Nat Standards File
	# Else, use newly created Standards File	
	natkeyID = add_default_nat_key_data(gkaFiles[1],natKeyStandardsFile)		
	if (productKeyBranch == "Y"):
		# Retrieve last used ID from TMPL_NAT_KEY and use to generate newest Nat_Key_ID
		newNatID = int(get_last_row(gkaFiles[1])[0]) + 1
		update_product_nat_key(gkaFiles[1],natKeyStandardsFile_SCD,newNatID)
		update_sub_dim_nat_standards(temp_subDimNatStandardsFile,natkeyID,newNatID)
		add_default_sub_dim_nat_data(gkaFiles[3],temp_subDimNatStandardsFile, prodNatKey=newNatID)
	else:
		update_sub_dim_nat_standards(temp_subDimNatStandardsFile,natkeyID)
		add_default_sub_dim_nat_data(gkaFiles[3],temp_subDimNatStandardsFile, geolocation=geolocation)

	optDimensions = raw_input("Enter \"PROMO\" or \"PROMODETAIL\" or \"BOTH\" or \"NONE\": ")

	if optDimensions == "PROMO":
		add_opt_dimensions(True,False,gkaFiles[3],temp_subDimNatStandardsFile)
	elif optDimensions == "PROMODETAIL":
		add_opt_dimensions(False,True,gkaFiles[3],temp_subDimNatStandardsFile)
	elif optDimensions == "BOTH":
		add_opt_dimensions(True,True,gkaFiles[3],temp_subDimNatStandardsFile)

	# objGrpScriptPath = os.getcwd()+"/ODS/objGroupFiller.sh"
	# # Change file permission to "Execute by Owner"
	# make_exec(objGrpScriptPath)
	# subprocess.call([objGrpScriptPath, SUB_NM, SUB_ID])

	# Clean-up
	# closeDeleteFiles(odsFiles)
	# closeDeleteFiles(gkaFiles)
	# os.rmdir(path)

	# Only works in dev-environment
	pushSeedData("GKA")
	pushSeedData("ODS")

	# Trigger cka_config_data_load.ksh to output to CKA DB
	subprocess.call([ckaDataLoad_script,newProcessDate])

	# MUST LOGIN TO ODS BEFORE TRIGGERING THIS SCRIPT
	# Trigger tlog_config_data_load.ksh to output to ODconfig
	# subprocess.call([odsDataLoad_script,processDate])

if __name__ == '__main__':
	main()
