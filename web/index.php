<html>
<head>
<?php
include(vars.php);
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
	<input type="radio" name="dist" value="fedora" checked>Fedora<br>
	<input type="radio" name="dist" value="ubuntu">Ubuntu<br>
	<input type="radio" name="dist" value="centos">CentOs<br>
	<input type="radio" name="dist" value="debian">Debian<br><br><hr><br>
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
