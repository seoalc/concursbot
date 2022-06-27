<?php
function getUserInfoByTGID ($tgId) {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "SELECT `username`, `firstname`, `lastname`, `patronymic` FROM `users` WHERE `tg_id` = " . $tgId;

	$query = mysqli_query($db, $sql);
	$row = mysqli_fetch_assoc($query);
	return $row;

	mysqli_close($db);
}

function getTextIdByTGID ($tgId) {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "SELECT `concurstextId` FROM `uspayconvid` WHERE `tg-id` = " . $tgId;

	$query = mysqli_query($db, $sql);
	$row = mysqli_fetch_assoc($query);
	return $row;

	mysqli_close($db);
}
