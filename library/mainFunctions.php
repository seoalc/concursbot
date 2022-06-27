<?php

function loadPage ($controllerName, $actionName = 'Index')
{
	// подключаем контроллер
	include_once PathPrefix . $controllerName . PathPostfix;

	// формируем название функции
	$function = $actionName.'Action';
	$function();
}

function loadTemplate ($templateName)
{
	include_once TemplatePrefix . $templateName . TemplatePostfix;
}

/**
 * Функция отладки. Останавливает работу программы, выводя значение переменной
 *
 * @param variant $value переменная вывода ее на страницу
 */
 function d ($value = null, $die = 1)
 {
	echo 'Debug: <br /><pre>';
	print_r($value);
	echo '</ pre>';

	if ($die) die;
 }

/**
 * Преобразорвание результата работы функции выборки в ассоциативный массив
 *
 * @param recordset $rs набор строк - результат работы SELECT
 * @return array
 */
function createSmartyRsArray($rs)
{
    if(! $rs) return false;

    $smartyRs = array();
    while ($row = mysqli_fetch_assoc($rs)) {
        $smartyRs[] = $row;
    }

    return $smartyRs;
}

/**
 * Функция редиректа на javascript
 *
 * @params $url - принимает параметром адрес куда нужно редиректнуть
 * @return ничего не возвращает, просто делает редирект
 */
function JSRedirect ($url) {
	echo '<script type="text/javascript">';
	echo 'window.location.href="'.$url.'";';
	echo '</script>';
}

/**
 * Функция проверки длины строки на допустимость
 *
 * @params $str - строка, которую нужно проверить
 * 			$min, $max - минимально и максимально допустимые значения
 * @return array
 */
function checkSrtLength ($str, $min, $max) {
	if (mb_strlen($str, 'UTF-8') < $min) {
		return 1;
	} elseif (mb_strlen($str, 'UTF-8') > $max) {
		return 2;
	} else {
		return 3;
	}
}
