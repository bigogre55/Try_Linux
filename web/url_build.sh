#!/bin/bash

vnc=$(echo $1 | tr ":" " ")

read -a add <<<$vnc
port=$(expr 5900 + ${add[1]})
sock=$(expr 6080 + ${add[1]})
vdir=$(expr 0 + ${add[1]})
./utils/launch.sh --listen $sock --vnc 10.0.0.24:$port --web /srv/novnc/$vdir >> /dev/null 2>&1 &
echo ":$sock/index.html?dir=$dir&port=$sock"
