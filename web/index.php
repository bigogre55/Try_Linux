<html>
<head>
<?php
include("vars.php");
?>
<style>
body {
	background-color: #CBC7BE;
}
#table {
        margin-top: 20px;
        background-color: white;
}
.choose {
	margin: auto;
	width: 45%;
	text-align: center;
	padding: 10px;
	border: 3px solid black;
}
<link rel="stylesheet" type="text/css" href="../mine/css/bootstrap.min.css" />
</style>
<title>Try Linux</title>
</head>
<body>
<div class="choose" id="table">
<form id="pick" action="build.php" onsubmit="please_wait()">
<h1>Choose a Distribution to try:</h1><br>
<?php
$responce = shell_exec('virsh pool-refresh --pool base_images');
$files = array();
$files = scandir($dir);
//echo $responce;
//print_r($files);
foreach ($files as $name) {
	$name = basename($name, ".img");
	if ($name == "." || $name == "..") {
		echo ""; //do nothing
	} else {
		echo "  <input type=\"radio\" name=\"dist\" value=\"$name\" checked>$name<br>\n";
	}
}
?>
Enter a Profile name:<br><br>
        <input type="text" name="name"><br><br>
        <input type="button" value="Launch" onclick="please_wait();go()"><br>
</form>
<p id="waitt"></p>
<p id="waitb"></p>
</div>
<script>
function go() {
	document.getElementById("pick").submit();
}
function please_wait() {
	document.getElementById("waitt").innerHTML = "Machine Generation can take up to two minutes";
	document.getElementById("waitb").innerHTML = "Please be patient; It is still loading...";
}
function keyboard_check(event) {
	if((event.keyCode == 13)) {
		please_wait()
	}
}
</script>
</body>
</html>
