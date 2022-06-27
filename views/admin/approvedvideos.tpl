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
          <h1>Страница с одобренными видео</h1>
        </div>
      </div>
    </div>
	</header>
	<section class="new-videos">

    <div class="wrapper">
			<div class="name">
					<h2>Видео, которые были одобрены вами.</h2>
			</div>
      <div class="items">
				<?php
				if (!empty($approvedVideos)) {
					foreach ($approvedVideos as $item) { ?>
						<div class="new-video-one">
								<div class="video-number">
										Заявка № <?php echo $item['id']; ?>
								</div>
								<h3><?php echo $item['text-name']; ?></h3>
								<div class="video-wrapprer">
								  <div class="video video-1">
								    <video controls>
								      <source src="/<?php echo $item['filePath']; ?>" type="video/mp4">
								      <source src="/files/users-videos/VID-20220126-WA0017.ogg" type="video/ogg">
								      Your browser does not support HTML5 video.
								    </video>

								  </div>
								</div>
								<div class="videoCapt">
										<div class="videoCapt-author">
												Автор видео: <b><?php echo $item['lastname']; ?> <?php echo $item['firstname']; ?> <?php echo $item['patronymic']; ?></b>
										</div>
										<div class="videoCapt-author-contact">
												Логин телеграм для связи - <?php echo $item['username']; ?>
										</div>
										<div class="videoCapt-author-nomination">
												Номинация <?php echo $item['nominationName']; ?>
										</div>
										<div class="videoCapt-textCapt">
												<p>
														<?php echo $item['text']; ?>
												</p>
										</div>
								</div>
						</div>
					<?php } ?>
				</div>
				<?php
				} else {
				?>
				<div class="">
					<h2>Еще нет одобренных вами видео в этом конкурсе</h2>
				</div>
				<?php } ?>
    </div>
  </section>
</body>
</html>
