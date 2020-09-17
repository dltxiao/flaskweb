#!/bin/bash

let log_id=`cat log_id`
content="This is a test log! 1234567890abcdef 1234567890abcdef 1234567890abcdef 1234567890abcdef 1234567890abcdef 1234567890abcdef 1234567"

lookup_disk_usage(){
	disk_usage=`df|grep HISTORY|awk -F " " '{print $5}'`
	echo "HistoryLog partition usaged: $disk_usage"
}

swallow_disk_space(){
	read -p "How much disk space do you want to swallow?(mb)" space_size
	dd if=/dev/zero of=$RANDOM.$space_size.mb
}

write_log(){
	read -p "How much system_log do you want to write:" log_number
	echo $log_number
	for i in {1..$log_number}
	do
		#write_syslog "LOG_TEST" "$log_id $content"
		echo "$log_id"
		let i++
		let log_id++
	done
}

write_log
