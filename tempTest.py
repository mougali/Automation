import os
import sys
import csv
import subprocess
import shutil

from subprocess import Popen, PIPE

# Global variables
inputDataDict = {}
processDate="20151112"
ODS_INPUT_DEST="/dsd_2/relr45d/tlog/data/inputs/config/"

# Set login credentials (for ODconfig)
userODS = 'AODR45ODCONFIGD'
pwdODS = 'odconfigaodr5dev'
sidODS = 'CMI280D'
schemaODS = 'AODR45ODCONFIGD'
od_connectionParam=userODS+"/"+pwdODS+"@"+sidODS

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
			sys.exit(1)
		except ValueError, msg:
			print msg
			print "Please ensure order-form is completely and accurately filled."
			sys.exit(1)

# Function that takes the sqlCommand and connectString and returns the queryResult and errorMessage (if any)
# CREDIT: https://moizmuhammad.wordpress.com/2012/01/31/run-oracle-commands-from-python-via-sql-plus/
def runSqlQuery(paramList):
	params = ['sqlplus', '-S', ]
	params += paramList
	session = Popen(params, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	return session.communicate()	

# Back-up original seedfiles in data/inputs/config/
# @param seedfileDirectory - Location/Directory of seedfiles in the environment.
# @param processDate - Date suffix of seedfile names. Used in naming of backup directory.
def backupSeedFiles(seedfileDirectory, processDate):

	# Make directory (named after processDate in YYYYMMDD) if doesn't exist
	destination=os.path.join(seedfileDirectory, processDate+"_BKP")
	if not os.path.exists(destination):
		os.makedirs(destination)

	# Get list of files in seedfileDirectory
	files = os.listdir(seedfileDirectory)

	# Move all relevant files (with original process-date) into backup folder
	for f in files:
		if f.endswith(processDate+".csv"):
			try:
				shutil.move(os.path.join(seedfileDirectory,f), destination)
			except IOError, msg:
				print IOError
				print msg

# Main function
def main():
	# inputFilePath = os.path.join(os.getcwd(), "OrderForm.csv")
	# loadInputData(inputFilePath)
	# global inputDataDict
	# for key, value in inputDataDict.iteritems():
	# 	print key + ": " + value

	# # Generate command-line statement to execute Config_Create_Backups.sql
	# cmd = [od_connectionParam, "@Config_Create_Backups.sql", "02dec2015"]
	# runSqlQuery(cmd)

	# Test backupSeedFiles function
	backupSeedFiles(ODS_INPUT_DEST, processDate)

if __name__ == '__main__':
		main()