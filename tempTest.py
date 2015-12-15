import os
import sys
import csv
import subprocess
import shutil

from subprocess import Popen, PIPE
from datetime import date, time, datetime
from collections import deque

# Global variables
inputDataDict = {}
processDate="20151112"
ODS_INPUT_DEST="/dsd_2/relr45d/tlog/data/inputs/config/"

origProcessDateObj=''	
origProcessDate=''		# E.g. "20150914"
origProcessDate_text=''	# E.g. "11sep2015"
newProcessDateObj=''
newProcessDate=''
newProcessDate_text=''
suffix=".csv"

date="16nov2015"

# Set login credentials (for ODconfig)
userODS = 'AODR45ODCONFIGD'
pwdODS = 'odconfigaodr5dev'
sidODS = 'CMI280D'
schemaODS = 'AODR45ODCONFIGD'
od_connectionParam=userODS+"/"+pwdODS+"@"+sidODS

SRC_CD='WAL'

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

# Load previous processing date and new date into global vars.
# @param datetimelogFilePath - Path of datetimelog.csv (stores previous processign datetimes)
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

# Unarchive seedfiles of given processDate from backup folder in data/inputs/config (ODS_INPUT_DEST).
# Prerequisites: Backup folder with given processDate exists.
# Post-requisite: All seedfiles from backup folder are pushed into data/inputs/config. Backup folder is deleted.
# @param processDate - Date in (YYYYMMDD) which matches suffix of relevant seedfiles.
def revertSeedData(processDate):
	path = os.path.join(ODS_INPUT_DEST,processDate)
	if os.path.isdir(path):
		# Push from src -> dest (backup folder --> ODS_INPUT_DEST)
		files = os.listdir(path)
		for f in files:
			if f.endswith(processDate+".csv"):
				try:
					shutil.move(os.path.join(path,f), ODS_INPUT_DEST)	# Move from back-up folder (path) --> data/inputs/config/
				except IOError, msg:
					print IOError
					print msg
	else:
		raise IOError(path + " not found!")

# Append records to TMPL_PRCS_CFG
# All records are generally the same, in the format: SUB_CD, 'N', '600'
# @param prcsCfgDataFile - Path of seedfile to be appended
def add_prcs_cfg_data(prcsCfgDataFile):
	f = open(prcsCfgDataFile, 'a')
	writer = csv.writer(f,quoting=csv.QUOTE_NONE,lineterminator=os.linesep)
	writer.writerow([SRC_CD,'N','600'])		


# Refreshes the OrderFormInfo.csv file.
def updateOrderFormInfo():
	

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
	# backupSeedFiles(ODS_INPUT_DEST, processDate)

	# Test loadDate function.
	# loc = os.path.join(os.getcwd(), 'datetimelog.csv')
	# loadDates(loc)
	# updateDates(loc, False)
	# loadDates(loc)

	# print origProcessDateObj
	# print newProcessDateObj

	# try:
	# 	revertSeedData(origProcessDate)
	# except IOError, msg:
	# 	print msg

	add_prcs_cfg_data(os.path.join(os.getcwd(),'TMPL_PRCS_CFG_20150914.csv'))

if __name__ == '__main__':
		main()