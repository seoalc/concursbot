// функция одобрения видео модером
function approveVideo(el) {
  id = el.id
  $.ajax({
  	method: "POST",
  	url: "/admin/approvevideo/",
    dataType: 'html',
  	data: { videoId: id },
    success: function(response){
      result = $.parseJSON(response);
      console.log(el.id)
  		$(el).parent().hide('slow');
      $(el).parent().siblings('.approvevideoSuccess').show('slow');
  	}
  });
}

// отмена одобрения только что одобренного видео модером
function approveCancelVideo(el) {
  id = el.id
  $.ajax({
  	method: "POST",
  	url: "/admin/approvecancelvideo/",
    dataType: 'html',
  	data: { videoId: id },
    success: function(response){
      result = $.parseJSON(response);
      console.log(el.id)
  		$(el).parent().hide('slow');
      $(el).parent().siblings('.videoManagmentButtons').show('slow');
  	}
  });
}

// указание причины перед отклонением видео
function sendReasonToDeclineVideo(el) {
  id = el.id
  $(el).parent().hide('slow');
  $(el).parent().siblings('.declinevideoReason').show('slow');
}
// отклонение видео модером
function declineVideo(el) {
  id = el.id
  // alert($(el).siblings('textarea').val())
  error = $(el).siblings('.error');
  if ($(el).siblings('textarea').val().length > 0) {
    error.remove();
  }
  if (!$(el).siblings('textarea').val()) {
    var error = document.createElement('div')
    error.className='error'
    error.style.color = 'red'
    error.innerHTML = 'Нельзя оставить это поле пустым'
    el.parentElement.insertBefore(error, el)
  } else {
    $.ajax({
    	method: "POST",
    	url: "/admin/declinevideo/",
      dataType: 'html',
    	data: { fileId: id , declineReason: $(el).siblings('textarea').val()},
      success: function(response){
        result = $.parseJSON(response);
        console.log(el.id)
        console.log(response)
    		$(el).parent().hide('slow');
        $(el).parent().siblings('.declinevideoSuccess').show('slow');
    	}
    });
  }
}

// отмена отклонения видео модером
function declinecancelVideo(el) {
  id = el.id
  $.ajax({
  	method: "POST",
  	url: "/admin/declinecancelvideo/",
    dataType: 'html',
  	data: { fileId: id },
    success: function(response){
      result = $.parseJSON(response);
      console.log(el.id)
  		$(el).parent().hide('slow');
      $(el).parent().siblings('.videoManagmentButtons').show('slow');
  	}
  });
}

/*-------------MENU-----------------*/
$('.nav-toggle').click(function(e) {

  e.preventDefault();
  $("html").toggleClass("openNav");
  $(".nav-toggle").toggleClass("active");

});

// выплывающее меню с подкатегориями
(function($) { // Begin jQuery
  $(function() { // DOM ready
    // If a link has a dropdown, add sub menu toggle.
    $('.button-dropdown').on("click", function(e) {
      $(this).siblings('.nav-dropdown').toggle();
      // Close one dropdown when selecting another
      $('.nav-dropdown').not($(this).siblings()).hide();
      e.stopPropagation();
    });
    // Clicking away from dropdown will remove the dropdown class
    $('html').on("click", function() {
      $('.nav-dropdown').hide();
    });

  }); // end DOM ready
})(jQuery); // end jQuery

var getAddTextForm = document.getElementById('add-text-form');

getAddTextForm.addEventListener('submit', function(event) {
  var i = 0;
  $('.add-text-block-textarea').each(function (index, element) {
    // index (число) - текущий индекс итерации (цикла)
    // данное значение является числом
    // начинается отсчёт с 0 и заканчивается количеству элементов в текущем наборе минус 1
    // element - содержит DOM-ссылку на текущий элемент

    var textEl = $(element).children('textarea').val();
    // if ($(element).find('input[type="radio"]:checked').val() != undefined) {
    //   inputVal = $(element).find('input[type="radio"]:checked').val();
    // }
    concursId = $(element).children('input[type="hidden"]').val();
    // console.log(concursId);
    if (i == 0) {
      if (textEl.length == 0) {
        $(element).siblings('.message').text('Должно быть заполнено')
        $(element).siblings('.message').show();
      } else if (textEl.length < 2) {
        $(element).siblings('.message').text('Название текста не может быть таким коротким')
        $(element).siblings('.message').show();
      } else {
        $(element).siblings('.message').hide();
      }
      textName = textEl
    } else if (i == 1) {
        if (textEl.length == 0) {
          $(element).siblings('.message').text('Должно быть заполнено')
          $(element).siblings('.message').show();
        } else if (textEl.length < 200) {
          $(element).siblings('.message').text('Текст для отображения на сайте слишком короткий')
          $(element).siblings('.message').show();
        } else {
          $(element).siblings('.message').hide();
        }
        textForWeb = textEl
    } else if (i == 2) {
        if (textEl.length == 0) {
          $(element).siblings('.message').text('Должно быть заполнено')
          $(element).siblings('.message').show();
        } else if (textEl.length < 200) {
          $(element).siblings('.message').text('Текст для бота слишком короткий')
          $(element).siblings('.message').show();
        } else {
          $(element).siblings('.message').hide();
        }
        textForBot = textEl
    } else if (i == 3) {
      inputVal = $(element).find('input[type="radio"]:checked').val();
      if (inputVal == undefined) {
        $(element).siblings('.message').text('Вы не выбрали номинацию')
        $(element).siblings('.message').show();
      } else {
        $(element).siblings('.message').hide();
      }
    } else if (i == 4) {
      inputValClass = $(element).find('input[type="radio"]:checked').val();
      if (inputValClass == undefined) {
        $(element).siblings('.message').text('Вы не выбрали категорию (класс)')
        $(element).siblings('.message').show();
      } else {
        $(element).siblings('.message').hide();
      }
    }
    i++;
  });
  if (textName.length > 2 & textForWeb.length > 200 & textForBot.length > 200) {
  // if ((textName.length > 30) && (textForWeb.length > 200) && (textForBot.length > 200) && (inputVal != undefined)) {
    if (inputVal == 1 || inputVal == 2 || inputVal == 3) {
        if (inputValClass == 1 || inputValClass == 2 || inputValClass == 3 || inputValClass == 4) {
            $.ajax({
                method: "POST",
                url: "/admin/addnewtext/",
                dataType: 'html',
                data: { concursId: concursId, textName: textName, textForWeb: textForWeb, textForBot: textForBot, nominationId: inputVal, classId: inputValClass },
                success: function(response){
                    result = $.parseJSON(response);
                    console.log(concursId);
                }
            });
            $('.approvevideoSuccess').show();
            $('#add-text-form')[0].reset();
            $('.approvevideoSuccess').hide(7000);
        }
    }
  }
	event.preventDefault();
});

// изменение текста
function editText(el) {
    var i = 0;
    $('.edit-text-block-textarea').each(function (index, element) {
        alert(i);
        i++;
    });
}
