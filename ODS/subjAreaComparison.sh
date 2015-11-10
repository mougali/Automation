#!/bin/bash

# Description: Compares contents of records within a specific OBJ,OBJ_GRP category against one another.
# The base_record is the one w/ SUB_NM='CAF' (if existent) or SUB_NM='TCG'; otherwise there's no base_record
# and the entire grouping will be displayed as record if there's any variations in the records (apart from field 1).
# @params
# $1 == SUB_NM (e.g. 'CAF')

# FILES
objGroupsFile='subjAreaFiller_queryFile.txt'
searchFile='subjAreaFiller_outfile.txt'
tempOutFile='subjAreaComparison_temp.txt'

# Other variables / parameters
SUB_NM=$1
comparator=''

# Perform search of each object type against $searchFile
objCount=$( wc -l ${objGroupsFile} | awk ' { print $1 } ' )
counter=1
objQuery=''
echo $objCount
while [ $counter -le $objCount ]
do
	objQuery=$( awk -F, -v var=$counter ' FNR==var { print $0 } ' ${objGroupsFile} )

	# perform search against $searchFile
	grep ${objQuery} ${searchFile} > $tempOutFile

	# remove first line from $tempOutFile
	sed '1d' $tempOutFile > tmpfile.txt; mv tmpfile.txt $tempOutFile

	# cat $tempOutFile
	printf "\n"

	# generate comparator
	comparator=$( awk -F, -v var=$SUB_NM ' BEGIN {ORS=","} { if ($1==var) for (i=2;i<=NF;i++) print $i } ' $tempOutFile )
	# printf "%s" $comparator
	# printf "\n"

	# perform comparison.
	# If a record doesn't equal to $baseRecord --> highlight it red
	# Temporary solution: print the variable.
	tempOutStr=$( cat $tempOutFile )
	if [ "$tempOutStr"!="" ]; then
		awk -F, -v var='' -v var1="${comparator}" ' BEGIN {ORS=","} { for (i=2;i<=NF;i++) var+="$i" } { print var } ' $tempOutFile
	fi

	awk -F, ' { print substr($0,index($0,$2)) } ' $tempOutFile

	printf "\n"

	let counter++
done