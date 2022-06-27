<?php
function getTextInfoById ($id) {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "SELECT `id`, `nomination-id`, `name`, `text`, `text-for-web`, `users-category` FROM `concurstexts` WHERE `id` = " . $id;

	$query = mysqli_query($db, $sql);
	$row = mysqli_fetch_assoc($query);
	return $row;

	mysqli_close($db);
}

function addNewText ($concursId, $textName, $textForWeb, $textForBot, $nominationId, $classId) {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "INSERT INTO `concurstexts` (`concurs-id`, `nomination-id`, `name`, `text`, `text-for-web`, `users-category`)";
	$sql .= " VALUES ({$concursId}, {$nominationId}, '{$textName}', '{$textForBot}', '{$textForWeb}', '{$classId}')";

	$query = mysqli_query($db, $sql);
	return $sql;

	mysqli_close($db);
}

function getTextsForModerById ($id) {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

	$sql = "SELECT `id`, `name`, `text-for-web` FROM `concurstexts` WHERE `modId` = " . $id;

	$query = mysqli_query($db, $sql);
	while ($row = mysqli_fetch_assoc($query)) {
		$rsArray[] = $row;
	}
	return $rsArray;

	mysqli_close($db);
}
