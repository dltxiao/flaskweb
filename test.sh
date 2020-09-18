#!/bin/bash

dir=.
area_split="----------------------------------"
let log_id=`cat log_id`
content="This is a test log! 1234567890abcdef 1234567890abcdef 1234567890abcdef 1234567890abcdef 1234567890abcdef 1234567890abcdef 1234567"

lookup_disk_usage(){
	disk_usage=`df|grep HISTORY|awk -F " " '{print $5}'`
	echo $area_split
	echo "HistoryLog partition usaged: $disk_usage"
	echo $area_split
	echo " "
}

lookup_oldest_file(){
	oldest_point_system=`ls $dir/system_log_*|awk -F "_" '{print $3}'|sort -r | tail -n 1`
	oldest_file_system=`ls $dir/system_log_*|grep $oldest_point_system`
	oldest_point_mgmt=`ls $dir/mgmt_log_*|awk -F "_" '{print $3}'|sort -r | tail -n 1`
	oldest_file_mgmt=`ls $dir/mgmt_log_*|grep $oldest_point_system`
	oldest_point_client=`ls $dir/client_audit_log_*|awk -F "_" '{print $4}'|sort -r | tail -n 1`
	oldest_file_client=`ls $dir/client_audit_log_*|grep $oldest_point_system`
	echo $area_split
	echo "Oldest file in HISTORY Partition is: $oldest_file_system"
	echo "Oldest file in HISTORY Partition is: $oldest_file_mgmt"
	echo "Oldest file in HISTORY Partition is: $oldest_file_client"
	echo $area_split
	echo " "
}

swallow_disk_space(){
	read -p "How much disk space do you want to swallow?(Mb) " space_size
	dd if=/dev/zero of=$dir/$RANDOM.$space_size.Mb bs=1M count=$space_size
	
	lookup_disk_usage	
}

write_log(){
	read -p "How much system_log do you want to write: " space
	let log_number=$space
	i=1
	while [ $i -le $log_number ] 
	do
		sh write_syslog.sh "LOG_TEST" "$log_id $content"
		let i++
		let log_id++
	done
	echo $log_id > log_id

	lookup_disk_usage
	lookup_oldest_file
}


while true
do
	echo $area_split
	echo "What do you want:"
	echo "1. Swallow some disk space."
	echo "2. Write a sort of system log."
	echo "3. Reset log id."
	echo "4. Lookup disk usage and oldest log file."
	echo "5. Quit."
	echo $area_split
	read -p "My choice is: " choice
	case $choice in
		1)
			swallow_disk_space;;
		2)
			write_log;;
		3)
			echo 0 > log_id;;
		4)
			lookup_disk_usage
			lookup_oldest_file;;
		5)
			break;;
		*)
			echo "Invalid choice"
	esac
done

