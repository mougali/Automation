import os, sys, stat
import errno, shutil
import subprocess
import csv

from collections import deque
from subprocess import Popen, PIPE

# Login information for databases and environments
userGKA="AODR45CKAADVD"
passwordGKA="ckaadvaodr5dev"
sidGKA="CKA280D"
connectionString=userGKA+"/"+passwordGKA+"@"+sidGKA

# Command to initiate and connect to SQL*PLUS
# sqlplus -S AODR45CKAADVD/ckaadvaodr5dev@CKA280D

userODS=""
passwordODS=""
sidODS=""
# End login information

# Table information for GKA
subTable="SUB_LOYALTYTEST"
subDimNatKeyTable="SUB_DIM_NAT_KEY_TYP_LOYALTYTEST"

# seed-file info (TEMPORARY)
subSeedName="TMPL_SUB_DATA_20150914.csv"

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

#function that takes the sqlCommand and connectString and returns the queryResult and errorMessage (if any)
# CREDIT: https://moizmuhammad.wordpress.com/2012/01/31/run-oracle-commands-from-python-via-sql-plus/
def runSqlQuery(sqlCommand, connectString):
   session = Popen(['sqlplus', '-S', connectString], stdin=PIPE, stdout=PIPE, stderr=PIPE)
   session.stdin.write(sqlCommand)
   return session.communicate()

def main():
	table = raw_input("Enter table-name for header file >>  ")
	seedFile = raw_input("Enter seed-file name >> ")
	seedFileLoc=os.getcwd()+"/Configuration Seed Files/GKA/"+seedFile

	query = createGkaQuery(table, seedFileLoc)
	print query + "\n\n"
	runSqlQuery(query, connectionString)

if __name__ == '__main__':
	main()
