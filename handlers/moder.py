from aiogram import types, Dispatcher
from bot_create import dp, bot
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.types.message import ContentType

import dbmain
import dbmoder
from keyboards import kb_moderbase

modID = None

# Получаем ID текущего члена жюри
# @dp.message_handler(commands=['moder'])
async def to_be_moder(message: types.Message):
    checkJury = dbmoder.checkModerByTgId(message.from_user.id)
    if checkJury == 1:
        global modID
        modID = message.from_user.id
        saluteText = "Привет, модератор " + message.from_user.first_name + "!\n\nВыберите действие, используя клавиатуру ниже"
        await bot.send_message(message.from_user.id, saluteText, reply_markup=kb_moderbase)

# @dp.message_handler(commands=['Смотреть новые неодобренные видео'])
async def get_not_approved_videos(message : types.Message):
    if message.from_user.id == modID:
        notApproved = dbmoder.getNotApprovedVideos()
        if len(notApproved) == 0:
            await bot.send_message(message.from_user.id, 'Новых видео для модерации нет')#, reply_markup=getnom_kb)
        else:
            for element in notApproved:
                videoCapt = '<b>Номинация:</b> ' + element['nominationName'] + '\n\n<b>Название:</b> ' + element['concurstextName']
                # клавиатура одобрить/отклонить
                approve = InlineKeyboardButton(text='Одобрить', callback_data='approve_'+str(element['id']))
                decline = InlineKeyboardButton(text='Отклонить', callback_data='decline_'+str(element['id']))
                approve_or_decline = InlineKeyboardMarkup(row_width=1).add(approve).add(decline)
                await bot.send_video(message.from_user.id, element['fileId'],
                                    caption=videoCapt,
                                    reply_markup=approve_or_decline,
                                    parse_mode=types.ParseMode.HTML)

# действия по нажатию инлайн кнопки одобрить
@dp.callback_query_handler(Text(startswith='approve_'))
async def approve_video(callback : types.CallbackQuery):
    if callback.from_user.id == modID:
        videoId = int(callback.data.split('_')[1])
        await dbmoder.setApproveStatus(videoId)
        await callback.answer('Вы одобрили видео' + str(videoId))


def register_handlers_moder(dp : Dispatcher):
    dp.register_message_handler(to_be_moder, commands=['moder'])
    dp.register_message_handler(get_not_approved_videos, Text(equals="смотреть новые неодобренные видео", ignore_case=True))
