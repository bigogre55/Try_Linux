<?php
$name = $_GET['name'];
$dist = $_GET['dist'];
shell_exec("./start.sh '$name' '$dist'");
$new_build = shell_exec("php domain_build.php '$name'");
file_put_contents("/srv/storage/virtual_machines/config.d/$name.xml",$new_build);
shell_exec("virsh create /srv/storage/virtual_machines/config.d/'$name'.xml > /dev/null 2>&1");
$vnc = shell_exec("virsh vncdisplay '$name'");
$url = shell_exec("./url_build.sh '$vnc'");
$date = date("Ymd-H:i:s");
shell_exec("touch /srv/storage/virtual_machines/MID/$name-$date.mid");
header("Location: https://www.jaketheogre.com".$url);
?>
