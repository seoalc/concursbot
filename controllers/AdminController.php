<?php

/**
 * Контроллер администраторов
 *
 */

// Подключаем модели
 include_once 'models/VideosModel.php';
 include_once 'models/UsersModel.php';
 include_once 'models/ConcurstextsModel.php';
 include_once 'models/ConcursesModel.php';
 include_once 'models/NominationsModel.php';

/**
 * Формирование главной страницы сайта
 *
 * @param object $smarty шаблонизатор
 */

 function indexAction () {
	if (isset($_SESSION['auth']) AND $_SESSION['auth'] == 1) {
		if ($_SESSION['status'] == 'admin') {
          $status = 'администратор';
        } else {
          $status = 'модератор';
        }

        $disapprovedVideos = getAllDisapprovedVideos();
        $i = 0;
        if ($disapprovedVideos) {
          foreach ($disapprovedVideos as $item) {
            // вытаскиваю инфо о пользователе по TG ID
            $userInfoForVideos = getUserInfoByTGID($item['tg_id']);
            $disapprovedVideos[$i]['username'] = $userInfoForVideos['username'];
            $disapprovedVideos[$i]['firstname'] = $userInfoForVideos['firstname'];
            $disapprovedVideos[$i]['lastname'] = $userInfoForVideos['lastname'];
            $disapprovedVideos[$i]['patronymic'] = $userInfoForVideos['patronymic'];
            // сначала выбираю id текста
            // $textId = getTextIdByTGID($item['tg_id']);
            // по id номинации вытаскиваю название номинации
            $nominationInfo = getNominationById($item['nominationId']);
            $disapprovedVideos[$i]['nominationName'] = $nominationInfo['name'];
            // по id текста ($item['concurstextId']) вытаскиваю инфу о тексте
            $textInfo = getTextInfoById($item['concurstextId']);
            $disapprovedVideos[$i]['id'] = $textInfo['id'];
            $disapprovedVideos[$i]['text-name'] = $textInfo['name'];
            $disapprovedVideos[$i]['text'] = $textInfo['text'];
            $i++;
          }
        }


		include_once 'views/admin/index.tpl';
	} else {
		include_once 'views/admin/login.tpl';
		unset($_SESSION['checkUsrWrong']);
	}

 }

 function approvevideoAction () {
   $videoId = $_POST['videoId'];

   approveVideoByTGID($videoId);

   echo json_encode($videoId);
 }

 function approvecancelvideoAction () {
   $videoId = $_POST['videoId'];

   approveCancelVideoByTGID($videoId);

   echo json_encode($videoId);
 }

 function declinevideoAction () {
   $fileId = $_POST['fileId'];
   $declineReason = $_POST['declineReason'];

   declineVideoByTGID($fileId, $declineReason);

   echo json_encode($declineReason);
 }

 function declinecancelvideoAction () {
   $fileId = $_POST['fileId'];

   declineCancelVideoByTGID($fileId);

   echo json_encode($fileId);
 }

 /**
  * Формирование страницы с новыми неодобренными видео
  *
  */

  function newvideosAction () {
     	if (isset($_SESSION['auth']) AND $_SESSION['auth'] == 1) {
     		if ($_SESSION['status'] == 'admin') {
           $status = 'администратор';
         } else {
           $status = 'модератор';
         }

         $disapprovedVideos = getAllDisapprovedVideos();
         $i = 0;
         foreach ($disapprovedVideos as $item) {
           // вытаскиваю инфо о пользователе по TG ID
           $userInfoForVideos = getUserInfoByTGID($item['tg_id']);
           $disapprovedVideos[$i]['username'] = $userInfoForVideos['username'];
           $disapprovedVideos[$i]['firstname'] = $userInfoForVideos['firstname'];
           $disapprovedVideos[$i]['lastname'] = $userInfoForVideos['lastname'];
           $disapprovedVideos[$i]['patronymic'] = $userInfoForVideos['patronymic'];
           // сначала выбираю id текста
           // $textId = getTextIdByTGID($item['tg_id']);
           // по id номинации вытаскиваю название номинации
           $nominationInfo = getNominationById($item['nominationId']);
           $disapprovedVideos[$i]['nominationName'] = $nominationInfo['name'];
           // по id текста ($item['concurstextId']) вытаскиваю инфу о тексте
           $textInfo = getTextInfoById($item['concurstextId']);
           $disapprovedVideos[$i]['id'] = $textInfo['id'];
           $disapprovedVideos[$i]['text-name'] = $textInfo['name'];
           $disapprovedVideos[$i]['text'] = $textInfo['text'];
           $i++;
         }

     		include_once 'views/admin/newvideos.tpl';
     	} else {
     		include_once 'views/admin/login.tpl';
     		unset($_SESSION['checkUsrWrong']);
     	}

  }

/**
   * Формирование страницы с одобренными данным модером видео
   *
   */

   function approvedvideosAction () {
      	if (isset($_SESSION['auth']) AND $_SESSION['auth'] == 1) {
      		if ($_SESSION['status'] == 'admin') {
            $status = 'администратор';
          } else {
            $status = 'модератор';
          }

          $approvedVideos = getAllApprovedVideosToModer();
          $i = 0;
          foreach ($approvedVideos as $item) {
            // вытаскиваю инфо о пользователе по TG ID
            $userInfoForVideos = getUserInfoByTGID($item['tg_id']);
            $approvedVideos[$i]['username'] = $userInfoForVideos['username'];
            $approvedVideos[$i]['firstname'] = $userInfoForVideos['firstname'];
            $approvedVideos[$i]['lastname'] = $userInfoForVideos['lastname'];
            $approvedVideos[$i]['patronymic'] = $userInfoForVideos['patronymic'];

            // по id номинации вытаскиваю название номинации
            $nominationInfo = getNominationById($item['nominationId']);
            $approvedVideos[$i]['nominationName'] = $nominationInfo['name'];
            // по id текста ($item['concurstextId']) вытаскиваю инфу о тексте
            $textInfo = getTextInfoById($item['concurstextId']);
            $approvedVideos[$i]['id'] = $textInfo['id'];
            $approvedVideos[$i]['text-name'] = $textInfo['name'];
            $approvedVideos[$i]['text'] = $textInfo['text'];
            $i++;
          }

      		include_once 'views/admin/approvedvideos.tpl';
      	} else {
      		include_once 'views/admin/login.tpl';
      		unset($_SESSION['checkUsrWrong']);
      	}

   }

   /**
      * Формирование страницы с добавлением текстов
      *
      */

      function addtextAction () {
         	if (isset($_SESSION['auth']) AND $_SESSION['auth'] == 1) {
         		if ($_SESSION['status'] == 'admin') {
               $status = 'администратор';
             } else {
               $status = 'модератор';
             }

             $currentConcursId = getCurrentConcursId();

         		include_once 'views/admin/addtext.tpl';
         	} else {
         		include_once 'views/admin/login.tpl';
         		unset($_SESSION['checkUsrWrong']);
         	}

      }

/**
    * Добавление нового текста в базу
    *
    */

    function addnewtextAction () {
        $textName = $_POST['textName'];
        $textForWeb = $_POST['textForWeb'];
        $textForBot = $_POST['textForBot'];
        $nominationId = $_POST['nominationId'];
        $concursId = $_POST['concursId'];
        $classId = $_POST['classId'];

        $sql = addNewText($concursId, $textName, $textForWeb, $textForBot, $nominationId, $classId);

        echo json_encode($sql);
    }

/**
    * Страница с текстами для редактирования
    *
    */

    function gettextsAction () {
      if (isset($_SESSION['auth']) AND $_SESSION['auth'] == 1) {
          if ($_SESSION['status'] == 'admin') {
              $status = 'администратор';
          } else {
              $status = 'модератор';
          }

          $texts = getTextsForModerById($_SESSION['adminId']);
          $i = 0;
          foreach ($texts as $item) {
              $minText = mb_substr($item['text-for-web'], 0, 130);
              $last = mb_substr($minText, -1);
              if ($last == '<') {
                  $minText = mb_substr($item['text-for-web'], 0, 129);
              } else if ($last == '>') {
                  $minText = mb_substr($item['text-for-web'], 0, 131);
              }
              $item['text-for-web'] = $minText;
              $texts[$i]['text-for-web'] = $minText;
              $i++;
          }
          include_once 'views/admin/gettexts.tpl';
        } else {
            include_once 'views/admin/login.tpl';
            unset($_SESSION['checkUsrWrong']);
        }
    }

/**
    * Страница с текстами для редактирования
    *
    */

    function edittextAction () {
       if (isset($_SESSION['auth']) AND $_SESSION['auth'] == 1) {
           if ($_SESSION['status'] == 'admin') {
              $status = 'администратор';
           } else {
              $status = 'модератор';
           }

           $textId = $_GET['id'];
           $textInfo = getTextInfoById($textId);
           include_once 'views/admin/edittext.tpl';
       } else {
          include_once 'views/admin/login.tpl';
          unset($_SESSION['checkUsrWrong']);
       }
    }
