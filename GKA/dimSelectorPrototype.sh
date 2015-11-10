#!/bin/bash

## In full program, should have this as a global variable
SUB_ID=55


# Parse through TMPL_DIM_DATA; transfer each dimension to an array 
# Display all dimensions from array
# arrLength=$(wc -l TMPL_DIM_DATA_20150914.csv | awk '{ print $1 }'}

dimArray=($(awk -F, '{print $2}' TMPL_DIM_DATA_20150914.csv))
dimIdArray=($(awk -F, '{print $1}' TMPL_DIM_DATA_20150914.csv))

destFile='TMPL_SUB_DIM_NAT_KEY_TYP_DATA_20150914.csv'

dim_index=-1
DIM_ID=-1

for i in "${dimArray[@]}"
do
	:
	echo $i
done	


## Ask user to select one of the above dimensions
echo -n "Please select one of the above dimensions for your client --> "
read dimSelection

## Validate input existence

counter=0
for i in "${dimArray[@]}"
do
	let counter+=1
	if [ "$i" == "$dimSelection" ]; then
		dim_index=$counter
		echo $dim_index
	fi
done

echo "Selected dimension has been found and validated. Now adding to system..."

## If match exists, add selected DIM_ID to TMPL_SUB_DIM_NAT_KEY_TYP_DATA: [ SUB_ID DIM_ID NAT_KEY_TYP_ID FRC_LKP PRE_KEY]

if [ $dim_index > -1 ]; then
	DIM_ID=$(echo ${dimIdArray[$dim_index]})
	# echo ${dimIdArray[$dim_index]}
	# echo $DIM_ID
	printf '%s,%s,%s,%s,%s\n' "$SUB_ID" "$DIM_ID" " " "Y" "N" >> ${destFile}
fi

## Based on selected dimension, display potential NAT_KEY_TYP_ID's that can be used
## This one's going to be a bit tougher. Need to know which NAT_KEY_TYP_IDs fall under which DIMENSIONS