from bot_create import dp, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import aioschedule
import dbother
import dbmain
from datetime import datetime, timedelta

from keyboards import first_kb, getnom_kb, loadvideo_kb, notsend_kb

async def noon_print():
    print("It's noon!")

async def payRemind():
    concursFinishDate = dbmain.getConcursesFinishDates()
    # tg-id всех наоплативших пользователей для рассылки им напоминания
    allNotpayUsersTGID = dbother.getAllNotpayUsersTGID()
    # перебор их в цикле и рассылка
    for el in allNotpayUsersTGID:
        payRemindMessage = 'Приветствую!\nНапоминаем о том, что в данный момент проходит конкурс, '\
                            'который продлится до '+ concursFinishDate +'. Успейте принять участие!'
        await bot.send_message(el['tg_id'], payRemindMessage, reply_markup=first_kb)
    print(allNotpayUsersTGID)

async def videosendRemind():
    concursFinishDate = dbmain.getConcursesFinishDates()
    # tg-id всех оплативших, но не записавших видео участников для рассылки напоминаний
    allNotvideosUsersTGID = dbother.getallNotvideosUsersTGID()
    # перебор их в цикле и рассылка
    for el in allNotvideosUsersTGID:
        payRemindMessage = 'Приветствую!\nНапоминаем о том, что в данный момент проходит конкурс, '\
                            'который продлится до '+ concursFinishDate +'. Вы оплатили участие, но еще не отправили нам видео\n\n'\
                            'Успейие выбрать номинацию и записать видео!'
        await bot.send_message(el['tg-id'], payRemindMessage, reply_markup=getnom_kb)
    print(allNotvideosUsersTGID)

async def videosendTimeRemind():
    current_datetime = datetime.now()
    # если месяц одинарный, добавляю ноль впереди
    if len(str(current_datetime.month)) == 1:
        monthNow = '0' + str(current_datetime.month)
    else:
        monthNow = str(current_datetime.month)
    # текущая дата для выборки текущего времени из базы (за сегодня именно)
    nowDate = str(current_datetime.year) + '-' + monthNow + '-' + str(current_datetime.day)
    timesForNowDate = dbother.getTimesForNowDate(nowDate)
    for element in timesForNowDate:
        textTakingTimeStrp = datetime.strptime(element['textTakingTime'], '%H:%M:%S')
        textTakingTimeStrf = datetime.strftime(textTakingTimeStrp, '%H:%M:%S')
        nowTimeStr = str(current_datetime.hour) + ':' + str(current_datetime.minute) + ':' + str(current_datetime.second)
        nowTimeStrp = datetime.strptime(nowTimeStr, '%H:%M:%S')
        differenceTime = nowTimeStrp - textTakingTimeStrp
        oneHour = timedelta(hours= 1 , minutes=00, seconds=00)
        oneHourSix = timedelta(hours= 1 , minutes=6, seconds=00)
        if differenceTime < oneHour:
            minutesKetti = str(differenceTime).split(':')
            minutesLeft = 60 - int(minutesKetti[1])
            if 27 < minutesLeft < 33:
                print('осталось меньше 30 минут')
                await bot.send_message(element['tg-id'], 'осталось '+ str(minutesLeft) +' минут чтобы записать и отправить видео', reply_markup=loadvideo_kb)
                if 8 < minutesLeft < 14:
                    print('осталось меньше 15 минут')
                    await bot.send_message(element['tg-id'], 'осталось '+ str(minutesLeft) +' минут чтобы записать и отправить видео', reply_markup=loadvideo_kb)
            elif 8 < minutesLeft < 14:
                print('осталось меньше 15 минут')
                await bot.send_message(element['tg-id'], 'осталось '+ str(minutesLeft) +' минут чтобы записать и отправить видео', reply_markup=loadvideo_kb)
            else:
                print('осталось больше минут')
        else:
            # чтобы сообщение о прошедшем часе выводилось только один раз
            if differenceTime < oneHourSix:
                print('час прошел уже епта')
                dbother.resetPaymentStatusForUser(element['tg-id'])
                get_payment_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Оплатить', callback_data='payform_'))
                ifNotSendVideoText = 'Прошло уже больше часа, к сожалению мы так и не получили от Вас видео'\
                                        'Теперь для повторного участия Вам нужно оплатить новый текст'
                await bot.send_message(element['tg-id'], ifNotSendVideoText, reply_markup=notsend_kb)
                # await bot.send_message(element['tg-id'], ifNotSendVideoText2, reply_markup=get_payment_kb)


async def scheduler():
    # aioschedule.every(1).minutes.do(payRemind)
    aioschedule.every().day.at("14:20").do(payRemind)
    aioschedule.every().day.at("14:30").do(videosendRemind)
    aioschedule.every(5).minutes.do(videosendTimeRemind)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
