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
					<h2>Отредактируйте нужные поля и нажмите сохранить.</h2>
			</div>
      <div class="items">
        <div class="edit-text">
					<div class="edit-text-block-for-web">
						<h3>1 Можете изменить название текста</h3>
						<hr>
						<div class="edit-text-block-textarea">
							<textarea class="text-name" id="text-name"><?php echo $textInfo['name']; ?></textarea>
						</div>
            <div class="message my-message" style="display: none">

            </div>
					</div>

          <div class="edit-text-block-for-web">
						<h3>2 Текст для отображения на сайте</h3>
						<hr>
						<div class="edit-text-block-textarea">
							<p>
								Для отображения на сайте текст нужно вводить с тегами html - &lt;br&gt;<br><br>
								Пример:<br>
								У лукоморья дуб зелёный;&lt;br&gt;<br>
								Златая цепь на дубе том:&lt;br&gt;
							</p>
							<textarea id="text-for-web"><?php echo $textInfo['text-for-web']; ?></textarea>
						</div>
            <div class="message my-message" style="display: none">
              Должно быть заполнено
            </div>
					</div>

          <div class="edit-text-block-for-web">
						<h3>3 Введите в поле текст для отображения в боте</h3>
						<hr>
						<div class="edit-text-block-textarea">
							<p>
								Для корректного отображения текста в боте теги использовать не нужно<br><br>
								Каждая новая строка начинается с переноса строки клавишей Enter<br>
							</p>
							<textarea id="text-for-bot"><?php echo $textInfo['text']; ?></textarea>
						</div>
						<div class="message my-message" style="display: none">
              Должно быть заполнено
            </div>
					</div>

          <div class="edit-text-block-for-web">
			  <h3>4 Номинация</h3>
			  <hr>
			  <dl class="edit-text-block-textarea">
				  <dd>
					  <label>
						  <?php if ($textInfo['nomination-id'] == 1) { ?>
							  <input type="radio" name="radio" checked value="1">
							  Поэзия
						  <?php } else {?>
							  <input type="radio" name="radio" value="1">
							  Поэзия
						  <?php } ?>
					  </label>
					  <label>
						  <?php if ($textInfo['nomination-id'] == 2) { ?>
							  <input type="radio" name="radio" checked value="2">
							  Проза
						  <?php } else {?>
							  <input type="radio" name="radio" value="2">
							  Проза
						  <?php } ?>
					  </label>
					  <label>
						  <?php if ($textInfo['nomination-id'] == 3) { ?>
							  <input type="radio" name="radio" checked value="3">
							  Драматургия
						  <?php } else {?>
							  <input type="radio" name="radio" value="3">
							  Драматургия
						  <?php } ?>
					  </label>
				  </dd>
			  </dl>
			  <div class="message my-message" style="display: none">
				  Должно быть выбрано
				</div>
		</div>

          <div class="edit-text-block-for-web">
			  <h3>5 Выберите категорию пользователя (класс)</h3>
			  <hr>
					  <div class="edit-text-block-textarea">
					    <div>
					      <label>
                  			<?php if ($textInfo['users-category'] == 0) { ?>
	  					        <input type="radio" name="radio2" checked value="0">
								1 категория (младшая группа)
                  			<?php } else {?>
	                    		<input type="radio" name="radio2" value="0">
	  					        1 категория (младшая группа)
                  			<?php } ?>
					      </label><br>
					      <label>
                  			<?php if ($textInfo['users-category'] == 1) { ?>
	  					        <input type="radio" name="radio2" checked value="1">
	  					        2 категория (средняя группа)
                  			<?php } else {?>
	                    		<input type="radio" name="radio2" value="1">
	  					        2 категория (средняя группа)
                  			<?php } ?>
					      </label><br>
							<label>
                  				<?php if ($textInfo['users-category'] == 2) { ?>
	  					        	<input type="radio" name="radio2" checked value="2">
	  					        	3 категория (старшая группа)
                  				<?php } else {?>
	                    			<input type="radio" name="radio2" value="2">
	  					        	3 категория (старшая группа)
                  				<?php } ?>
					      	</label><br>
                			<label>
                  			<?php if ($textInfo['users-category'] == 3) { ?>
	  					        <input type="radio" name="radio2" checked value="3">
	  					        4 категория (взрослая группа)
                  			<?php } else {?>
	                    		<input type="radio" name="radio2" value="3">
	  					        4 категория (взрослая группа)
                  			<?php } ?>
					      </label>
					    </div>
					  </div>
					  <div class="message my-message" style="display: none">
						  Должно быть выбрано
					  </div>
					</div>

          <div class="textManagmentButtons">
            <div class="approvevideoSuccess" style="display: none">
              Вы одобрили это видео
            </div>
            <button class="textManagmentButtons-btn1 btn-1" onclick="editText(this); return false;">
              Отправить
            </button>
          </div>
				</div>
      </div>

    </div>
  </section>
</body>
</html>
