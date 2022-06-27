<?php

/**
 * Контроллер главной страницы
 *
 */

// Подключаем модели
 //include_once 'models/CategoriesModel.php';
 //include_once 'models/BattinfoModel.php';

/**
 * Формирование главной страницы сайта
 *
 * @param object $smarty шаблонизатор
 */
 //d ($function);

 function indexAction ()
 {
	if (isset($_SESSION['auth']) AND $_SESSION['auth'] == 1) {
		//$crypt = crypt("Maxim89m", "hg56ij89erf45dh");
		//d($crypt);
		include_once 'views/default/index.tpl';
	} else {
		include_once 'views/default/login.tpl';
		unset($_SESSION['checkUsrWrong']);
	}

 }
