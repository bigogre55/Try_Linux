#!/bin/bash
list=$(ls /srv/storage/virtual_machines/MID/)
read -a nlist <<<$list
for n in ${nlist[@]}
do
vnc=$(echo $n | tr '.-' " ")
read -a fil <<<$vnc
now=`date`
name=${fil[0]}
read -a tim <<<$now
StartDate=$(date -u -d "${fil[2]}" +"%s")
FinalDate=$(date -u -d "${tim[3]}" +"%s")
uup=$(date -u -d "0 $FinalDate sec - $StartDate sec"  +"%H:%M:%S")
uup="$uup"".00"
up=$(echo "$uup" | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }')
if [ $up -gt 7200 ]; then
	virsh destroy $name > /dev/null &2>1 &
	virsh vol-delete $name.img --pool base_images > /dev/null &2>1 &
	rm -rf /srv/storage/virtual_machines/MID/$n
fi
done
