#!/bin/bash

## Definitely need to modify the regex statement
## Finds in .csv the appropriate datafile (specified by $pattern), and replaces the SUB_ID w/ new client id

SUB_ID=$1
pattern=$2
grep $pattern TMPL_OBJ_DATA_20150914.csv | awk -F, -v var=$SUB_ID '{ gsub(/[A-Z]*[a-z]*/,var,$1); print $0 }'


## NEXT STEP: append modified record into seed-file 
