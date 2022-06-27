from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# первая клавиатура модератора с базовым функционалом
b1 = KeyboardButton('Смотреть новые неодобренные видео')
kb_moderbase = ReplyKeyboardMarkup(resize_keyboard=True)
kb_moderbase.add(b1)
