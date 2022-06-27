from aiogram import types, Dispatcher
from bot_create import dp, bot
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.types.message import ContentType

import dbmain
import dbjury
from keyboards import kb_newvid

juryID = None

get_new_videos_inline = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Новые видео категории поэзия', callback_data='newvideos_1'))\
                                                            .add(InlineKeyboardButton(text='Новые видео категории проза', callback_data='newvideos_2'))\
                                                            .add(InlineKeyboardButton(text='Новые видео категории драматургия', callback_data='newvideos_3'))



# Получаем ID текущего члена жюри
# @dp.message_handler(commands=['jury'])
async def to_be_jury(message: types.Message):
    checkJury = dbjury.checkJuryByTgId(message.from_user.id)
    if checkJury == 1:
        global juryID
        juryID = message.from_user.id
        saluteText = "Привет, " + message.from_user.first_name + "!\n\nВыберите номинацию, видео в которой хотите оценить"
        await bot.send_message(message.from_user.id, saluteText, reply_markup=get_new_videos_inline)

# по нажатию инлайн кнопки с номинацией, подгружаются видео этой номинации без голоса текущего члена жюри
@dp.callback_query_handler(Text(startswith='newvideos_'))
async def get_new_videos_by_nomination(callback : types.CallbackQuery):
    if callback.from_user.id == juryID:
        nominationId = int(callback.data.split('_')[1])
        allNewVideosByNomination = dbjury.getAllNewVideos(callback.from_user.id, nominationId)
        for element in allNewVideosByNomination:
            videoCapt = '<b>Номинация:</b> ' + element['nominationName'] + '\n\n<b>Название:</b>\n' + element['textName']\
                        + '\n\nДля отправки своей оценки (от 1 до 10) используйте кнопки ниже'
            # кнопка с голосами для отправки
            v1 = InlineKeyboardButton(text='1', callback_data='voice_1_'+str(element['id']))
            v2 = InlineKeyboardButton(text='2', callback_data='voice_2_'+str(element['id']))
            v3 = InlineKeyboardButton(text='3', callback_data='voice_3_'+str(element['id']))
            v4 = InlineKeyboardButton(text='4', callback_data='voice_4_'+str(element['id']))
            v5 = InlineKeyboardButton(text='5', callback_data='voice_5_'+str(element['id']))
            v6 = InlineKeyboardButton(text='6', callback_data='voice_6_'+str(element['id']))
            v7 = InlineKeyboardButton(text='7', callback_data='voice_7_'+str(element['id']))
            v8 = InlineKeyboardButton(text='8', callback_data='voice_8_'+str(element['id']))
            v9 = InlineKeyboardButton(text='9', callback_data='voice_9_'+str(element['id']))
            v10 = InlineKeyboardButton(text='10', callback_data='voice_10_'+str(element['id']))
            send_voice_for_video = InlineKeyboardMarkup(row_width=1).row(v1, v2, v3, v4, v5).row(v6, v7, v8, v9, v10)
            await bot.send_video(callback.from_user.id, element['fileId'],
                                caption=videoCapt,
                                reply_markup=send_voice_for_video,
                                parse_mode=types.ParseMode.HTML)
        await callback.answer()

# по нажатию инлайн кнопки с цифрой, эта цифра отправляется как оценка
@dp.callback_query_handler(Text(startswith='voice_'))
async def send_voice_for(callback : types.CallbackQuery):
    if callback.from_user.id == juryID:
        voice = int(callback.data.split('_')[1])
        videoId = int(callback.data.split('_')[2])
        await dbjury.sendVoiceFor(voice, videoId, callback.from_user.id)
        await callback.answer()

def register_handlers_jury(dp : Dispatcher):
    dp.register_message_handler(to_be_jury, commands=['jury'])
    # dp.register_message_handler(get_new_videos, Text(equals="новые видео", ignore_case=True))
