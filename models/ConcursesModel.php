<?php
function getCurrentConcursId () {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "SELECT `id` FROM `concurses` WHERE `active` = 1";

	$query = mysqli_query($db, $sql);
	$row = mysqli_fetch_row($query);
	return $row;

	mysqli_close($db);
}
