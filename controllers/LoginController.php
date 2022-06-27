<?php

/**
 * Контроллер работы с пользователями
 *
 */

// Подключаем модели
 // include_once 'models/UsersModel.php';
 include_once 'models/AdminsModel.php';

/**
 * Формирование главной страницы сайта
 *
 * @param object $smarty шаблонизатор
 */

 function indexAction ()
 {
	// проверка на пустоту поля с именем пользователя и паролем
	if (!empty($_POST['login']) AND !empty($_POST['password'])) {
		// проверка имени пользователя на допустимые символы
		// допустимы только буквы, цифры и символы -_
		$checkLoginSymb = checkLoginSymb($_POST['login']);
		if ($checkLoginSymb == 1) {
			$checkPass = checkPassSymb($_POST['password']);
			if ($checkPass == 1) {
				//если к введенным логину и паролю нет никаких претензий
				//сравниваем их с теми, что в базе
				//$crypt = crypt("Inter123", "hg56ij89erf45dh");
				//var_dump($crypt);
				$checkLoginContrast = checkAdminLoginContrast($_POST['login']);
				// если пользователь с таким именем есть в базе, продолжаем с ним работу
				// если нет, выводим ошибку
				if ($checkLoginContrast == 1 or $checkLoginContrast == 2) {
					// переводим пароль в хэш и сравниваем с тем, что в базе
					// в случае несовпадения, выдаем ошибку о неверном пароле
					$cryptPass = crypt($_POST['password'], "hg56ij89erf45dh");
					$checkPassContrast = checkAdminPassContrast($_POST['password']);
					if ($checkPassContrast == 1 or $checkPassContrast == 2) {
						$_SESSION['auth'] = 1;
                        if ($checkPassContrast == 1) {
                          $_SESSION['status'] = 'admin';
                        } elseif ($checkPassContrast == 2) {
                          $_SESSION['status'] = 'moder';
                        } else {
                          $_SESSION['status'] = 'nobody';
                        }

                        // $_SESSION['admId'] = $checkPassContrast['tg-id'];
						$userData = getAdminByLogin($_POST['login'], $_SESSION['status']);
						$_SESSION['adminId'] = $userData['tg-id'];
						// $_SESSION['fio'] = $userData['fio'];
						// $_SESSION['username'] = $userData['username'];
						// $_SESSION['privilegies'] = $userData['privilegies'];

						/*$unitData = getUnitById($userData['unitId']);
						$_SESSION['unitId'] = $userData['unitId'];
						$_SESSION['unitName'] = $unitData['unitName'];
						$_SESSION['abbreviation'] = $unitData['abbreviation'];
						$_SESSION['higherDivision'] = $unitData['higherDivision'];
						$_SESSION['graphName'] = $unitData['graphName'];*/
						JSRedirect('/admin/');
					} else {
						$_SESSION['checkUsrWrong'] = "Вы ввели неверный пароль";
						JSRedirect('/admin/');
					}
				} else {
					$_SESSION['checkUsrWrong'] = "Пользователь с таким именем не найден";
					JSRedirect('/admin/');
				}
			} else {
				$_SESSION['checkUsrWrong'] = "Вы использовали в пароле недопустимые символы";
				JSRedirect('/admin/');
			}
		} else {
			$_SESSION['checkUsrWrong'] = "Вы использовали в логине недопустимые символы. Допустимы только буквы, цифры и символы - и _";
			JSRedirect('/admin/');
		}
	} else {
		// если поле с именем пользователя или пароля пустое, выдаем ошибку
		$_SESSION['checkUsrWrong'] = "Вы не ввели имя пользователя или пароль!";
		JSRedirect('/admin/');
	}

 }

 function checkLoginSymb ($login) {
	 if (preg_match('/^[a-zA-Z][a-zA-Z0-9-_]{1,20}$/', $login)) {
		return 1;
	} else {
		return 2;
	}
 }

 function checkPassSymb ($password) {
	/*if (preg_match('/(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$/', $password)) {
		return 1;
	} else {
		return 2;
	}*/
	if (preg_match('/[0-9A-Za-z_!@#=%-]{6,14}$/', $password)) {
		return 1;
	} else {
		return 2;
	}
 }

/**
 * Выход из аккаунта
 *
 * @param ничего не принимает, просто уничтожение сессии и редирект на главную
 */

 function logoutAction ()
 {
	session_destroy ();

	JSRedirect ("/");

 }
