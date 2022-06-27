from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


#кнопка клавиатуры для регистрации
b1 = KeyboardButton('Зарегистрироваться')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1)

# кнопка для пропуска шага в машине состояний
b2 = KeyboardButton('Пропустить')
skip_step = ReplyKeyboardMarkup(resize_keyboard=True)
skip_step.add(b2)

# клавиатура с приветствием (согласие на участие и правила)
b3 = KeyboardButton('Да! Хочу участвовать!')
b4 = KeyboardButton('Читать правила')
salute_kb = ReplyKeyboardMarkup(resize_keyboard=True)
salute_kb.add(b3)

# клавиатура с кнпками номинаций, для получения текста
b5 = KeyboardButton('Получить текст номинации поэзия')
b6 = KeyboardButton('Получить текст номинации проза')
b7 = KeyboardButton('Получить текст номинации драматургия')
getnom_kb = ReplyKeyboardMarkup(resize_keyboard=True)
getnom_kb.add(b5).add(b6).add(b7).add(b4)

# клавиатура с кнопкой загрузки нового видео
b8 = KeyboardButton('Загрузить видео')
loadvideo_kb = ReplyKeyboardMarkup(resize_keyboard=True)
loadvideo_kb.add(b8).add(b4)

# клавиатура проверки статуса своего видео
b9 = KeyboardButton('Статус моего видео')
loadedvideo_kb = ReplyKeyboardMarkup(resize_keyboard=True)
loadedvideo_kb.add(b9).add(b4)


b10 = KeyboardButton('отмена')
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_kb.add(b10)

# первоначальная клавиатура пользователя с кнопками согласен и редактировать лич данные
b11 = KeyboardButton('Согласен')
b12 = KeyboardButton('Редактировать личные данные')
first_kb = ReplyKeyboardMarkup(resize_keyboard=True)
first_kb.add(b11).add(b12)

# клавиатура в случае если не успел записать видео в течение часа
b13 = KeyboardButton('Заполнить заявку заново')
notsend_kb = ReplyKeyboardMarkup(resize_keyboard=True)
notsend_kb.add(b13)
