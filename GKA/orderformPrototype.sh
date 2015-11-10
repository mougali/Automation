#!/bin/bash

subDataFile='TMPL_SUB_DATA_20150914.csv'

echo -n "Would you like to append ('App') or delete ('Del')? "
read choice

echo $choice

if [ ${choice} = "App" ]; then
	echo -n "Enter New Client ID: "
	read SUB_ID

	echo -n "Enter New Client Name: "
	read SUB_NM

	echo -n "Enter New Client Description: "
	read SUB_DESC

	printf '%s,%s,%s\n' "\"$SUB_ID\"" "\"$SUB_NM\"" "\"$SUB_DESC\"" >> ${subDataFile}


	echo "--------------FILE APPEND VALIDATION--------------"
	cat ${subDataFile}
	echo "\n"

elif [ ${choice} = "Del" ]; then
	cp ${subDataFile} temp.csv
	sed '$ d' temp.csv > ${subDataFile}

	echo "--------------FILE DELETE VALIDATION--------------"
	cat ${subDataFile}
	echo "\n"
fi