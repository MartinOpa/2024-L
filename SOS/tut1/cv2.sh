#!bin/bash

path="$HOME/opt/SOS"
input="seznam-obci-cr.txt"

if [ ! -d "$path" ]; then
    mkdir -p "$path"
fi

while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" == *ova* && "$line" != *Nova* ]]; then
	folder=$(echo "$line" | tr ' ' '_')
	mkdir -p "$path"/"$folder"
	
	list_file="${path}/${folder}/list.txt"
	touch ${list_file}
	
	letter="${folder:0:1}"
	
	find "$path" -maxdepth 1 -name "${letter}*" -printf "%f\n" > "$list_file"    
    fi
done < "$input"
