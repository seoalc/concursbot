<?php
function getAllDisapprovedVideos () {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "SELECT `tg_id`, `fileId`, `concurstextId`, `nominationId`, `filePath` FROM `videos` WHERE `status` = 0";

	$query = mysqli_query($db, $sql);
	$query0 = mysqli_num_rows($query);
	if ($query0 > 0) {
		while ($row = mysqli_fetch_assoc($query)) {
	    $rsArray[] = $row;
		}
	} else {
		$rsArray = Null;
	}

	return $rsArray;

	mysqli_close($db);
}

function approveVideoByTGID ($videoId) {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "UPDATE `videos` SET `status` = 1, `approveModerId` = " . $_SESSION['adminId'] . " WHERE `fileId` = '" . $videoId . "'";

	$query = mysqli_query($db, $sql);

	mysqli_close($db);
}

function approveCancelVideoByTGID ($videoId) {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "UPDATE `videos` SET `status` = 0, `approveModerId` = 0 WHERE `fileId` = '" . $videoId . "'";

	$query = mysqli_query($db, $sql);

	mysqli_close($db);
}

function declineVideoByTGID ($fileId, $declineReason) {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "UPDATE `videos` SET `status` = 3, `declineReason` = '" . $declineReason . "' WHERE `fileId` = '" . $fileId . "'";

	$query = mysqli_query($db, $sql);

	mysqli_close($db);
}

function declineCancelVideoByTGID ($fileId) {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "UPDATE `videos` SET `status` = 0, `declineReason` = 'empty' WHERE `fileId` = '" . $fileId . "'";

	$query = mysqli_query($db, $sql);

	mysqli_close($db);
}

function getAllApprovedVideosToModer () {
	$db = mysqli_connect("localhost", "root", "pass", "concurs-testbot");

  $sql = "SELECT `tg_id`, `fileId`, `concurstextId`, `nominationId`, `filePath` FROM `videos` WHERE `status` = 1 AND `approveModerId` = " . $_SESSION['adminId'];

	$query = mysqli_query($db, $sql);
	$query0 = mysqli_num_rows($query);
	if ($query0 > 0) {
		while ($row = mysqli_fetch_assoc($query)) {
	    $rsArray[] = $row;
		}
	} else {
		$rsArray = Null;
	}
	return $rsArray;

	mysqli_close($db);
}
