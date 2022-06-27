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
	<section class="add-text">

    <div class="wrapper">
			<div class="name">
					<h2>Заполните все поля и нажмите ОТПРАВИТЬ.</h2>
			</div>
      <div class="items">
        <form class="add-text-form" id="add-text-form" action="" method="post">
					<div class="add-text-block-for-web">
						<h3>1 Введите в поле название текста</h3>
						<hr>
						<div class="add-text-block-textarea">
							<textarea placeholder="Название текста..." class="text-name"></textarea>
						</div>
            <div class="message my-message" style="display: none">

            </div>
					</div>

					<div class="add-text-block-for-web">
						<h3>2 Введите в поле текст для отображения на сайте</h3>
						<hr>
						<div class="add-text-block-textarea">
							<p>
								Для отображения на сайте текст нужно вводить с тегами html - &lt;br&gt;<br><br>
								Пример:<br>
								У лукоморья дуб зелёный;&lt;br&gt;<br>
								Златая цепь на дубе том:&lt;br&gt;
							</p>
							<textarea placeholder="Строка<br> Строка<br>"></textarea>
						</div>
            <div class="message my-message" style="display: none">
              Должно быть заполнено
            </div>
					</div>

					<div class="add-text-block-for-web">
						<h3>3 Введите в поле текст для отображения в боте</h3>
						<hr>
						<div class="add-text-block-textarea">
							<p>
								Для корректного отображения текста в боте теги использовать не нужно<br><br>
								Каждая новая строка начинается с переноса строки клавишей Enter<br>
							</p>
							<textarea placeholder="Текст без тегов для бота"></textarea>
						</div>
						<div class="message my-message" style="display: none">
              Должно быть заполнено
            </div>
					</div>

					<div class="add-text-block-for-web">
						<h3>4 Выберите номинацию</h3>
						<hr>
					  <dl class="add-text-block-textarea">
					    <dd>
					      <label>
					        <input type="radio" name="radio" value="1">
					        Поэзия
					      </label>
					      <label>
					        <input type="radio" name="radio" value="2">
					        Проза
					      </label>
								<label>
					        <input type="radio" name="radio" value="3">
					        Драматургия
					      </label>
					    </dd>
					  </dl>
						<div class="message my-message" style="display: none">
              Должно быть выбрано
            </div>
					</div>

          <div class="add-text-block-for-web">
						<h3>5 Выберите категорию пользователя (класс)</h3>
						<hr>
					  <div class="add-text-block-textarea">
					    <div>
					      <label>
					        <input type="radio" name="radio2" value="0">
					        1 категория (младшая группа)
					      </label><br>
					      <label>
					        <input type="radio" name="radio2" value="1">
					        2 категория (средняя группа)
					      </label><br>
								<label>
					        <input type="radio" name="radio2" value="2">
					        3 категория (старшая группа)
					      </label><br>
                <label>
					        <input type="radio" name="radio2" value="3">
					        4 категория (взрослая группа)
					      </label>
					    </div>
					  </div>
						<div class="message my-message" style="display: none">
              Должно быть выбрано
            </div>
					</div>

          <div class="add-text-block-for-web">
            <div class="add-text-block-textarea">
              <input type="hidden" name="concursId" value="<?php echo $currentConcursId[0]; ?>">
            </div>
          </div>
          <div class="textManagmentButtons">
            <div class="approvevideoSuccess" style="display: none">
              Вы одобрили это видео
            </div>
            <button class="textManagmentButtons-btn1 btn-1">
              Отправить
            </button>
          </div>
				</form>
      </div>

    </div>
  </section>
</body>
</html>
