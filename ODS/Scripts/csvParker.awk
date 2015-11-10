awk 'NR==30{a[$0]=1;next} {n=0;for(i in a){if($0~i){n=1}}} n' filenames.txt TMPL_OBJ_DATA_20150914.csv
