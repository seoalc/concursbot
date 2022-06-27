<!DOCTYPE html>
<html>
<head>
	<title>Вход в личный кабинет</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<meta name="description" content="Вход в панель личного кабинета">
	<meta name="keywords" content="">
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<link rel="shortcut icon" href="/favicon.ico" >
	<!--Подключение стилей-->
	<link rel="stylesheet" href="/templates/default/css/login.css" />
	<link rel="stylesheet" href="/templates/default/css/responsive.css" />
</head>

<body>
	<div class="centro">
		<?php
		if (isset($_SESSION['checkUsrWrong'])) {
			echo $_SESSION['checkUsrWrong'];
		}

		?>
	</div>

	<div class="login-page">
		<div class="form">
			<div class="centro"><b>Панель администратора</b></div>
			<form class="login-form" action="/login/" method="post">
				<input type="text" name="login" placeholder="имя пользователя"/>
				<input type="password" name="password" placeholder="пароль"/>
				<button>войти</button>
			</form>
			<br><br><div class="centro"><a href="/admin/">панель администратора</a></div>
		</div>
	</div>
</body>
</html>
