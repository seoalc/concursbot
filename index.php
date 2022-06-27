<?php
session_start ();

include_once 'config/config.php';
//include_once 'config/db.php';
include_once 'library/mainFunctions.php';

// определяем контроллер, который будет подключен
if (isset($_GET['controller']))
{
	$controllerName = ucfirst($_GET['controller']);
}
else
{
	$controllerName = 'Index';
}

// определяем функцию в контроллере, с которой работать
$actionName = isset($_GET['action']) ? $_GET['action'] : 'index';

loadPage($controllerName, $actionName);
