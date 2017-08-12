#!/bin/bash

vnc=$(echo $1 | tr ":" " ")

read -a add <<<$vnc
port=$(expr 5900 + ${add[1]})
sock=$(expr 6080 + ${add[1]})
dir=$(expr 0 + ${add[1]})
/etc/novnc/utils/launch.sh --listen $sock --vnc 10.0.0.24:$port --cert /srv/novnc/novnc.pem --web /srv/novnc/$dir >> /var/log/nginx/novnc.$dir.log 2>&1 &
echo ":$sock/index.html?dir=$dir&port=$sock"
