<?php
function getNominationById ($nominationId) {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "SELECT `name` FROM `nominations` WHERE `id` = " . $nominationId;

  $query = mysqli_query($db, $sql);
	$row = mysqli_fetch_assoc($query);
	return $row;

	mysqli_close($db);
}
