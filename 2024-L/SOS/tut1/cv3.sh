#!bin/bash

path="$HOME/opt/SOS/rand"
num=$(( 1000 + $(( RANDOM % 1000 )) ))

if [ ! -d "$path" ]; then
    mkdir -p "$path"
fi

for ((i = 0; i < num; i++)); do
    filename=$((RANDOM))
    filepath="${path}/${filename}.txt"
    touch ${filepath}
    
    letter="${filename:0:1}"
    
    find "$path" -maxdepth 1 -name "${letter}*" -printf "%f\n" > "$filepath"
done
