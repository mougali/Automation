#!/bin/bash

COUNTER=0
while [ $COUNTER -lt 132 ]; do
	awk 'NR=='"$COUNTER"'{a[$0]=1;next} {n=0;for(i in a){if($0~i){n=1}}} n' filenames.txt TMPL_OBJ_DATA_20150914.csv > Grouped_Records/outfile_${COUNTER}.csv
	let COUNTER+=1
done