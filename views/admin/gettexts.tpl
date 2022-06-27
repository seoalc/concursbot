<!DOCTYPE html>
<html>
<head>
	<title>Панель администратора бота</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<meta name="description" content="Панель администратора бота">
	<meta name="keywords" content="">
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<link rel="shortcut icon" href="/favicon.ico" >

	<!--Подключение стилей-->
	<link rel="stylesheet" href="/templates/default/css/styles.css" />
	<link rel="stylesheet" href="/templates/default/css/leftmenu.css" />

	<!--Подключение js-->
	<script defer src="/templates/default/js/jquery-3.6.0.min.js"></script>
	<script defer src="/templates/default/js/myscripts.js"></script>
</head>

<body>
	<!-- <div class="debug">
			<div>
				<div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
				</div>
			</div>
	</div> -->
	<?php include_once('primary-nav.tpl'); ?>
	<header class="page-name">
    <div class="wrapper">
      <div class="items">
        <div class="page-name-one">
          <h1>Добавление новых текстов для участников конкурса</h1>
        </div>
      </div>
    </div>
	</header>
	<section class="get-texts">
    <div class="wrapper">
			<div class="name">
					<h2>Ниже представлены добавленные вами текста.</h2>
			</div>
      <div class="items">
        <!-- <div class="text-preview">
          <div class="text-name">
            <h3>Письмо Татьяны к Онегину (отрывок из романа «Евгений Онегин»)</h3>
          </div>
          <div class="text-preview-txt">
            Я к вам пишу — чего же боле?<br>
            Что я могу еще сказать?<br>
            Теперь, я знаю, в вашей воле<br>
            Меня презреньем наказать.<br>
          </div>
          <a href="#" class="text-preview-button">Редактировать</a>
        </div> -->
        <?php foreach ($texts as $item) {?>
          <div class="text-preview">
            <div class="text-name">
              <h3><?php echo $item['name']; ?></h3>
            </div>
            <div class="text-preview-txt">
              <?php echo $item['text-for-web']; ?>
            </div>
            <a href="/admin/edittext/<?php echo $item['id']; ?>/" class="text-preview-button">Редактировать</a>
          </div>
        <?php } ?>
      </div>

    </div>
  </section>
</body>
</html>
