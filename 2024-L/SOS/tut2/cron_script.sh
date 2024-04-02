#!bin/bash
time=$(date +'%Y-%m-%d %H:%M:%S')
file="/usr/local/bin/cron_time.txt"

if [ ! -f "$file" ]; then
	touch "$file"
fi

echo "$time" > "$file"

