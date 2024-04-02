#!/bin/bash

dir="/etc"
timestamp=$(date +'%Y_%m_%d_%H:%M:%S')
backup_dir="/backup"
backup="${backup_dir}/backup_$(timestamp)"

if [ ! -d ${backup_dir} ]; then
	mkdir ${backup_dir}
fi

tar -cf "$backup" "$dir"
