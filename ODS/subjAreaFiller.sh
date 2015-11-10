#!/bin/bash

## Description: Creates and appends new-client records for TMPL_SBJ_AREA_DATA. 
## Matches OBJECT and OBJECT_GRP fields w/ those of previous client; modifies these records
## to contain its own SUB_NM and appends it to the end of the seed-file.

# FILES and PARAMETERS
SUB_NM=$1
procDate='20150914'
seedFile='TMPL_SBJ_AREA_DATA_'$procDate'.csv'
outFile='subjAreaFiller_outfile.txt'
queryFile='subjAreaFiller_queryFile.txt'

# Store records in temporary file.
tempObjRecords='temp_objRecords.txt'
touch $tempObjRecords

awk -F, -v var=${SUB_NM} '{ if( $1 == var ) print $0 }' ${seedFile} | tee ${tempObjRecords}

# Parse through temp-file. Match up object w/ previously entered object from 
# seed-file.
touch $queryFile
awk -F, '{ print $2,$3 }' OFS=',' ${tempObjRecords} | tee ${queryFile}

printf '\n'

# Get number of records and store in variable $totalRecordCount
totalRecordCount=$( wc -l ${queryFile} | awk '{print $1}')
echo $totalRecordCount
printf '\n'

touch $outFile
printf "" > $outFile
counter=1
# Find all matching records and store in $outFile
while [ ${counter} -le ${totalRecordCount} ]
do
	matchRecords=$( awk -F, -v var=$counter ' FNR==var { print $0 } ' ${queryFile} )
	printf '%s----------------------\n' $matchRecords >> $outFile

	awk -F, -v var=$( echo $matchRecords | cut -d, -f 1 ) -v var1=$( echo $matchRecords | cut -d, -f 2 ) -v var3="$outFile" '{ if( $2==var && $3==var1 ) print $0 >> var3 }' ${seedFile}
	printf '\n\n' >> $outFile

	let counter++
done

# Display contents of program output (stored in $outFile)
cat $outFile

# Cleanup
rm ${tempObjRecords}