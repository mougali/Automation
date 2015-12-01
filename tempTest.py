import os
import sys
import csv

# Global variables
inputDataDict = {}

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

def main():
	inputFilePath = os.path.join(os.getcwd(), "OrderForm.csv")
	loadInputData(inputFilePath)
	global inputDataDict
	for key, value in inputDataDict.iteritems():
		print key + ": " + value

if __name__ == '__main__':
		main()