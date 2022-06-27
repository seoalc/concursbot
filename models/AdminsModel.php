<?php
function getAdminByLogin ($login, $status) {
	if ($status == 'admin') {
		$sql = "SELECT * FROM `admins` WHERE `login` = '{$login}'";
	} else {
		$sql = "SELECT * FROM `moders` WHERE `login` = '{$login}'";
	}

	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

	$query = mysqli_query($db, $sql);
	$row = mysqli_fetch_assoc($query);
	return $row;

	mysqli_close($db);
}

function getAdminNameById ($id) {
	$sql = "SELECT `fio2` FROM `admins` WHERE `id` = '{$id}'";
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

	$query = mysqli_query($db, $sql);
	$row = mysqli_fetch_assoc($query);
	return $row;

	mysqli_close($db);
}

function checkAdminLoginContrast($login) {
		$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot") or die("Ошибка " . mysqli_error($db));

		$query2 = mysqli_query($db, "SELECT * FROM `admins` WHERE `login` = '{$login}'");
		$rows2 = mysqli_num_rows($query2);

		$query = mysqli_query($db, "SELECT * FROM `moders` WHERE `login` = '{$login}'");
		$rows = mysqli_num_rows($query);
		if ($rows2 > 0) {
			return 1;
		} elseif ($rows > 0) {
			return 2;
		} else {
			return 3;
		}

		mysqli_close($db);
}

function checkAdminPassContrast ($pass) {
		$cryptPass = crypt($pass, "hg56ij89erf45dh");
		$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot") or die("Ошибка " . mysqli_error($db));

		$query2 = mysqli_query($db, "SELECT * FROM `admins` WHERE `password` = '{$cryptPass}'");
		$rows2 = mysqli_num_rows($query2);

		$query = mysqli_query($db, "SELECT * FROM `moders` WHERE `password` = '{$cryptPass}'");
		$rows = mysqli_num_rows($query);
		if ($rows2 > 0) {
			return 1;
		} elseif ($rows > 0) {
			return 2;
		} else {
			return 3;
		}

		mysqli_close($db);
}
