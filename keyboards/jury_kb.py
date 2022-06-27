from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#кнопка клавиатуры для регистрации
b1 = KeyboardButton('Новые видео')
kb_newvid = ReplyKeyboardMarkup(resize_keyboard=True)
kb_newvid.add(b1)
