<?php

// Константы для обращения к контроллерам
define('PathPrefix', 'controllers/');
define('PathPostfix', 'Controller.php');

//> используемый шаблон
$template = 'default';
$templateAdmin = 'admin';

//пути к файлам шаблонов (.tpl)
define('TemplatePrefix', "views/{$template}/");
define('TemplateAdminPrefix', "views/{$templateAdmin}/");
define('TemplatePostfix', '.tpl');

//пути к файлам шаблонов в вебпростарнстве
define('TemplateWebPath', "templates/{$template}/");
define('TemplateAdminWebPath', "/templates/{$templateAdmin}/");
//<
