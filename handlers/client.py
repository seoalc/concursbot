from aiogram import types, Dispatcher
from bot_create import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType

from config import PAYMENTS_TOKEN

from datetime import datetime
import random
import re
import urllib.request

from keyboards import kb_client, skip_step, salute_kb, getnom_kb, loadvideo_kb, loadedvideo_kb, cancel_kb, first_kb
import dbmain

# кнопка со ссылкой на правила проекта на сайте
rules_kb = InlineKeyboardMarkup(row_width=1)
blink = InlineKeyboardButton(text='Читать правила', url='http://site.ru')
rules_kb.add(blink)

# @dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    try:
        global tg_id
        tg_id = message.from_user.id
        usinfo = dbmain.checkIspolnByTgId(tg_id)
        if usinfo == 1:
            userPayment = dbmain.checkPaymentOfUser(tg_id)
            if userPayment == 1:
                saluteText = 'Приветствую, ' + message.from_user.first_name +\
                '\n\nВы уже произвели взнос\n\nГотовы получить текст и записать видео?'
                await bot.send_message(message.from_user.id, saluteText, reply_markup=getnom_kb)
            else:
                # saluteText = 'Приветствую, ' + message.from_user.first_name +\
                # '\nХотите поучаствовать в конкурсе?\nЕсли не знаете как, можете ознакомиться с правилами'
                # await bot.send_message(message.from_user.id, saluteText, reply_markup=salute_kb)
                await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы\n\n'\
                'Для участия в конкурсе после оплаты Вам будет выслан текст, по которму в течение одного '\
                'часа Вам нужно будет записать видео.\n\nТекст представляет собой отрывок из какого-либо произведения.'\
                '\nПобедителя определяют члены жюри\nУдачи!'\
                '\n\nМожете отредактировать свои личные данные.', reply_markup=first_kb)
        elif usinfo == 0:
            startMess = 'Добро пожаловать, ' + message.from_user.first_name + '!\nВашего аккаунта нет в системе. Желаете зарегистрироваться?'\
                        '\n\nПеред регистрацией нужно ознакомиться с правилами проекта. Регистрируясь здесь, Вы принимаете правила проекта.'
            await bot.send_message(message.from_user.id, startMess, reply_markup=rules_kb)
            await bot.send_message(message.from_user.id, '.', reply_markup=kb_client)
        else:
            await bot.send_message(message.from_user.id, 'Что-то пошло не так... Обратитесь к администратору')
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/mypizzalikebot')

class FSMNewuser(StatesGroup):
    firstname = State()
    lastname = State()
    patronymic = State()
    birthDate = State()
    kind = State()
    phoneNumber = State()
    vkLink = State()
    education_institution = State()
    teacher = State()

# Начало дилога загрузки при регистрации нового участника
# @dp.message_handler(commands=['Зарегистрироваться'], state=None)
async def command_register(message : types.Message):
    await FSMNewuser.firstname.set()
    await message.reply('Введите Ваше реальное имя', reply_markup=ReplyKeyboardRemove())

# Выход из состояний
# @dp.message_handler(state="*", commands="отмена")
# @dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

# Ловим первый ответ и пишем в словарь
# @dp.message_handler(state=FSMNewuser.firstname)
async def get_firstname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tg_id'] = message.from_user.id
        data['username'] = message.from_user.username
        data['firstname'] = message.text
    await FSMNewuser.next()
    await message.reply("Введите фамилию")

# Ловим второй ответ
# @dp.message_handler(state=FSMNewuser.lastname)
async def get_lastname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] = message.text
    await FSMNewuser.next()
    await message.reply("Введите отчество")

# Ловим третий ответ
# @dp.message_handler(state=FSMNewuser.patronymic)
async def get_patronymic(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['patronymic'] = message.text
    await FSMNewuser.next()
    await message.reply("Введите Вашу дату рождения в формате ДД-ММ-ГГГГ\nНапример, 01-01-1990")

# Ловим дату рождения
# @dp.message_handler(state=FSMNewuser.birthDate)
async def get_birthDate(message: types.Message, state: FSMContext):
    # получаю возраст пользователя на основе его даты рождения для добавления его в кортеж
    birth_date = datetime.strptime(message.text, '%d-%m-%Y')
    now_date = datetime.today()
    age = int(((now_date.year*10000 + now_date.month*100+now_date.day) - (birth_date.year*10000 + birth_date.month*100+birth_date.day)) / 10000)
    # для заноса даты в таблицу MySQL необходимо привести ее к формату ГГГГ-ММ-ДД
    birth_date = datetime.strftime(birth_date, '%d-%m-%Y')
    birth_date_tmp = str(birth_date).split('-')
    birth_date_new = birth_date_tmp[2] + '-' + birth_date_tmp[1] + '-' + birth_date_tmp[0]
    async with state.proxy() as data:
        data['birthDate'] = birth_date_new
        data['age'] = age
    await FSMNewuser.next()
    await message.reply("Введите цифру класса, в котором учитесь\n\nПропустите шаг, если закончили школу", reply_markup=skip_step)

# Ловим класс учебы
# @dp.message_handler(state=FSMNewuser.kind)
async def get_kind(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Пропустить':
            data['kind'] = 0
        else:
            data['kind'] = int(message.text)

        # В зависимости от класса школы или его отсутствия присваиваю пользователя к какой-либо категории
        if 1 <= data['kind'] <= 4:
            data['users-category'] = 1
        elif 5 <= data['kind'] <= 11:
            data['users-category'] = 2
        elif data['kind'] == 0:
            data['users-category'] = 3
    await FSMNewuser.next()
    await message.reply("Введите Ваш контактный номер телефона", reply_markup=ReplyKeyboardRemove())

# Ловим номер телефона
# @dp.message_handler(state=FSMNewuser.phoneNumber)
async def get_phoneNumber(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phoneNumber'] = message.text
    await FSMNewuser.next()
    await message.reply("Оставьте ссылку на Ваш профиль в социальной сети вконтакте (при наличии)\nНапример vk.com/perechitairf\n\nЛибо пропустите шаг", reply_markup=skip_step)

# Ловим ссылку на vk
# @dp.message_handler(state=FSMNewuser.vkLink)
async def get_vkLink(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Пропустить':
            data['vkLink'] = 'empty'
        else:
            data['vkLink'] = message.text
    await FSMNewuser.next()
    await message.reply("Укажите образовательное учреждение, в котором вы учитесь.\n"\
                        "Если вы не учитесь, то укажите от какой организации вы участвуете.\n\nВ ином случае пропустите этот шаг", reply_markup=skip_step)

# Ловим школу
# @dp.message_handler(state=FSMNewuser.education_institution)
async def get_education_institution(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Пропустить':
            data['education_institution'] = 0
        else:
            data['education_institution'] = message.text
    await FSMNewuser.next()
    await message.reply("Укажите ФИО вашего руководителя, для подготовки грамот в случае Вашей победы. Либо пропустите этот шаг\n\n"\
                        "ФИО руководителя в родительном падеже.\n\nНапример, Иванову Петру Алексеевичу")

# Ловим ФИО учителя
# @dp.message_handler(state=FSMNewuser.teacher)
async def get_teacher(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Пропустить':
            data['teacher'] = 0
        else:
            data['teacher'] = message.text

    # async with state.proxy() as data:
    #     await message.reply(str(data))
    await dbmain.addNewUser(state)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Вы успешно зарегистрированы\n\n'\
                            'Для участия в конкурсе после оплаты Вам будет выслан текст, по которму в течение одного '\
                            'часа Вам нужно будет записать видео.\n\nТекст представляет собой отрывок из какого-либо произведения.'\
                            '\nПобедителя определяют члены жюри\nУдачи!'\
                            '\n\nМожете отредактировать свои личные данные.', reply_markup=first_kb)

# @dp.message_handler(commands=['Редактировать личные данные'])
async def edit_users_self_data(message : types.Message):
    tg_id = message.from_user.id
    usinfo = dbmain.checkIspolnByTgId(tg_id)
    if usinfo == 1:
        # кнопка с выбором тех данных, которые нужно отредактировать
        usData1 = InlineKeyboardButton(text='Имя', callback_data='usData_firstname')
        usData2 = InlineKeyboardButton(text='Фамилия', callback_data='usData_lastname')
        usData3 = InlineKeyboardButton(text='Отчество', callback_data='usData_patronymic')
        usData4 = InlineKeyboardButton(text='Дата рождения', callback_data='usData_birthDate')
        usData5 = InlineKeyboardButton(text='Цифра класса учебы', callback_data='usData_kind')
        usData6 = InlineKeyboardButton(text='Номер телефона', callback_data='usData_phone')
        usData7 = InlineKeyboardButton(text='Ссылка на профиль соц сети вконтакте', callback_data='usData_vkLink')
        usData8 = InlineKeyboardButton(text='Учебное заведение/организация', callback_data='usData_educationInstitution')
        usData9 = InlineKeyboardButton(text='ФИО учителя/руководителя', callback_data='usData_teacher')
        send_usData_for_edit = InlineKeyboardMarkup(row_width=1).row(usData1, usData2, usData3).row(usData4).row(usData5)\
                                                    .row(usData6).row(usData7).row(usData8).row(usData9)
        await bot.send_message(message.from_user.id, 'Выберите какой из пунктов анкеты хотите отредактировать', reply_markup=send_usData_for_edit)

class FSMGotoeditusdata(StatesGroup):
    updtdata = State()
# по нажатию инлайн кнопки с выбранным параметром для редактирования,
# название этого параметра (str) отправится в базу
@dp.callback_query_handler(Text(startswith='usData_'))
async def send_users_data_for_edit(callback : types.CallbackQuery):
    tg_id = callback.from_user.id
    usinfo = dbmain.checkIspolnByTgId(tg_id)
    if usinfo == 1:
        # объявляю глобальные переменные для передачи в машину состояний
        # dataName это само название редактируемого поля в таблице с данными пользователя
        # usersDataByDataName это значение этого поля из таблицы, которое он хочет изменить
        global changeSuccessText
        global dataName
        dataName = callback.data.split('_')[1]
        if dataName == 'firstname':
            changeAlert = 'Последний раз Вы указали имя - '
            changeSuccessText = 'Ваше имя изменено на - '
        elif dataName == 'lastname':
            changeAlert = 'Последний раз Вы указали фамилию - '
            changeSuccessText = 'Ваша фамилия изменена на - '
        elif dataName == 'patronymic':
            changeAlert = 'Последний раз Вы указали отчество - '
            changeSuccessText = 'Ваше отчество изменено на - '
        elif dataName == 'birthDate':
            changeAlert = 'Последний раз Вы указали дату рождения - '
            changeSuccessText = 'Ваша дата рождения изменена на - '
            dataName = 'birth-date'
        elif dataName == 'kind':
            changeAlert = 'Последний раз Вы указали номер класса - '
            changeSuccessText = 'Ваш номер класса изменен на - '
        elif dataName == 'phone':
            changeAlert = 'Последний раз Вы указали номер телефона - '
            changeSuccessText = 'Ваш номер телефона изменен на - '
        elif dataName == 'vkLink':
            changeAlert = 'Последний раз Вы указали ссылку на свой профиль в социальной сети вконтакте - '
            changeSuccessText = 'Ссылка на Ваш профиль социальной сети вконтакте изменен на - '
            dataName = 'vk-link'
        elif dataName == 'educationInstitution':
            changeAlert = 'Последний раз Вы указали школу/учреждение - '
            changeSuccessText = 'Ваша школа/учреждение изменено на - '
            dataName = 'education-institution'
        elif dataName == 'teacher':
            changeAlert = 'Последний раз Вы указали ФИО учителя/руководителя - '
            changeSuccessText = 'ФИО учителя/руководителя изменены на - '
        usersDataByDataName = dbmain.getUsersDataByDataName(dataName, tg_id)
        dateFind = re.findall("(\d{4}-\d{2}-\d{2})", str(usersDataByDataName[dataName]))
        if len(dateFind) == 1:
            # для вывода даты пользователю необходимо привести ее к формату ДД-ММ-ГГГГ
            birth_date = datetime.strftime(usersDataByDataName[dataName], '%Y-%m-%d')
            birth_date_tmp = str(birth_date).split('-')
            birth_date_new = birth_date_tmp[2] + '-' + birth_date_tmp[1] + '-' + birth_date_tmp[0]
            usersDataByDataName[dataName] = birth_date_new
        await FSMGotoeditusdata.updtdata.set()
        await bot.send_message(callback.from_user.id, changeAlert + str(usersDataByDataName[dataName]) + \
                                '\n\nВведите новое значение', reply_markup=cancel_kb)
        await callback.answer()

# Продолжение машинного состояния по ловле изменяемого параметра личных данных пользователя
# @dp.message_handler(state=FSMGotoeditusdata.updtdata)
async def get_new_user_data(callback : types.CallbackQuery, state: FSMGotoeditusdata):
    async with state.proxy() as data:
        data['tg-id'] = callback.from_user.id
        data['userData'] = callback.text
        data['dataName'] = dataName
    print(callback.from_user.id)
    await dbmain.updtUsersInfo(state)
    await state.finish()
    await bot.send_message(callback.from_user.id, changeSuccessText + data['userData'], reply_markup=first_kb)

# @dp.message_handler(commands=['Согласен'])
async def send_videoinstruction(message : types.Message):
    tg_id = message.from_user.id
    usinfo = dbmain.checkIspolnByTgId(tg_id)
    if usinfo == 1:
        videoCapt = 'Для участия в конкурсе посмотрите видеоинструкцию.'
        await bot.send_video(message.from_user.id, 'BAACAgIAAxkBAAIKMGIFQm88seaiEJdxYPVF4rsIdRxRAAJbEAACCJmhS3IOjf480hdwIwQ',
                            caption=videoCapt,
                            reply_markup=salute_kb)
        await bot.send_message(message.from_user.id, 'А также можете еще раз ознакомиться с правилами на нашем сайте по ссылке ниже\n\n'\
                                                        'Когда будете готовы, нажмите кнопку "Да! Хочу участвовать!"', reply_markup=rules_kb)

# @dp.message_handler(commands=['Читать правила'])
async def send_rules_for_user(message : types.Message):
    tg_id = message.from_user.id
    usinfo = dbmain.checkIspolnByTgId(tg_id)
    if usinfo == 1:
        await bot.send_message(message.from_user.id, 'Для участия в конкурсе после оплаты Вам будет выслан текст, по которму в течение одного '\
        'часа Вам нужно будет записать видео.\n\nТекст представляет собой отрывок из какого-либо произведения.\nПобедителя определяют члены жюри\nУдачи!')

get_payment_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Оплатить', callback_data='payform_'))

# @dp.message_handler(commands=['да! хочу участвовать!'])
async def apply_part(message : types.Message):
    tg_id = message.from_user.id
    usinfo = dbmain.checkIspolnByTgId(tg_id)
    if usinfo == 1:
        userPayment = dbmain.checkPaymentOfUser(tg_id)
        if userPayment == 1:
            print(userPayment)
            saluteText = '\n\nВы уже произвели взнос, но не получали по нему текст\n\nГотовы получить текст и записать видео?'
            await bot.send_message(message.from_user.id, saluteText, reply_markup=getnom_kb)
        elif userPayment == 0:
            await bot.send_message(message.from_user.id, 'Нужно оплатить взнос.\n\n'\
            'Организационный взнос составляет 500 рублей за участие в одной номинации.', reply_markup=get_payment_kb)
            print(userPayment)
        else:
            saluteText = '\n\nВы уже получили текст\n\nУ вас осталось '+ str(userPayment) +' минут, чтобы записать по нему видео'
            await bot.send_message(message.from_user.id, saluteText, reply_markup=loadvideo_kb)

@dp.callback_query_handler(text='payform_')
async def pay_command(callback : types.CallbackQuery):
    userPayment = dbmain.checkPaymentOfUser(callback.message.chat.id)
    if userPayment == 1:
        saluteText = '\n\nВы уже произвели взнос, но не получали по нему текст\n\nГотовы получить текст и записать видео?'
        await bot.send_message(callback.from_user.id, saluteText, reply_markup=getnom_kb)
    elif userPayment == 0:
        await bot.send_invoice(callback.message.chat.id,
                                title='Платеж',
                                description='Платеж за участие в конкурсе',
                                provider_token=PAYMENTS_TOKEN,
                                currency='rub',
                                need_email=True,
                                need_phone_number=True,
                                prices=PRICES,
                                start_parameter='example',
                                payload='some_invoice')
    else:
        saluteText = '\n\nВы уже получили текст\n\nУ вас осталось '+ str(userPayment) +' минут, чтобы записать по нему видео'
        await bot.send_message(callback.from_user.id, saluteText, reply_markup=loadvideo_kb)

@dp.shipping_query_handler(lambda q: True)
async def shipping_process(shipping_query: ShippingQuery):
    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True
    )

@dp.pre_checkout_query_handler(lambda q: True)
async def pay_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def success_pay(message: Message):
    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(
            total_amount=message.successful_payment.total_amount // 100,
            currency=message.successful_payment.currency
        ),
        reply_markup=getnom_kb
    )

    usId = message.from_user.id
    concursId = 1
    # получаю отдельно текущую дату со временем, дату и время в разные переменные
    dateTimeReady_tmp = str(datetime.now()).split('.')
    dateTimeReady = dateTimeReady_tmp[0]
    dateTime_tmp = dateTimeReady.split(' ')
    dateOne = dateTime_tmp[0]
    timeOne = dateTime_tmp[1]
    await dbmain.addNewPayment(usId, concursId, dateTimeReady, dateOne, timeOne)


PRICES = [
    LabeledPrice(label='Конкурс', amount=50000)
]

finConcurs = dbmain.getConcursesFinishDates()
successful_payment = '''
Ура! Платеж на сумму `{total_amount} {currency}` совершен успешно! Желаем победы в конкурсе!\n\n
Выберите номинацию, в которой хотите поучаствовать и Вам будет отправлен текст, по которму нужно будет в течение часа записать видео.\n
'''
successful_payment = successful_payment + 'Конкурс продлится до '  + finConcurs + ', успейте записать видео.\n'
MESSAGES = {
    'successful_payment': successful_payment
}

# @dp.message_handler(commands=['получить текст номинации поэзия', 'получить текст номинации проза', 'получить текст номинации драматургия'])
async def get_poetry_text(message : types.Message):
    tg_id = message.from_user.id
    usinfo = dbmain.checkIspolnByTgId(tg_id)
    # usStatus = dbmain.checkUserStatus(tg_id)
    payStatus = dbmain.checkPaymentStatus(tg_id)
    if usinfo == 1:
        userPayment = dbmain.checkPaymentOfUser(tg_id)
        if userPayment == 1:
            userHaveText = dbmain.checkHavingText(tg_id)
            if userHaveText != 0:
                nominationName = message.text.split(' ')
                warningText = '''
                Вы уже получили текст, ждем от Вас видео\n\n
                У Вас осталось меньше часа для записи видео и отправки его сюда
                '''
                await bot.send_message(message.from_user.id, warningText, reply_markup=loadvideo_kb)
            else:
                nominationName = message.text.split(' ')
                if nominationName[3] == 'поэзия':
                    nominationId = 1
                elif nominationName[3] == 'проза':
                    nominationId = 2
                elif nominationName[3] == 'драматургия':
                    nominationId = 3
                # вытаксиваю из базы все тексты данной номинации
                concursText_tmp = dbmain.getRandomTextByNominationId(nominationId)
                # беру рандомный индекс из полученного списка
                random_index = random.randint(0, len(concursText_tmp) - 1)
                concursText = concursText_tmp[random_index]['name'] + '\n\n' + concursText_tmp[random_index]['text']

                # получаю отдельно текущую дату со временем, дату и время в разные переменные
                dateTimeReady_tmp = str(datetime.now()).split('.')
                dateTimeReady = dateTimeReady_tmp[0]
                dateTime_tmp = dateTimeReady.split(' ')
                dateOne = dateTime_tmp[0]
                timeOne = dateTime_tmp[1]
                await dbmain.updtUspayconvid(tg_id, concursText_tmp[random_index]['id'], concursText_tmp[random_index]['nomination-id'], dateOne, timeOne)

                warningText = '''
                Вы получили текст, ждем от Вас видео\n\n
                Не забудьте, что с момепнта получения текста у Вас есть ровно час на запись видео и отправку его сюда
                '''
                await bot.send_message(message.from_user.id, concursText)#, reply_markup=getnom_kb)
                await bot.send_message(message.from_user.id, warningText, reply_markup=loadvideo_kb)
        elif userPayment == 0:
            await bot.send_message(message.from_user.id, 'Нужно оплатить взнос.\n\n'\
            'Организационный взнос составляет 500 рублей за участие в одной номинации.', reply_markup=get_payment_kb)
        else:
            saluteText = '\n\nВы уже получили текст\n\nУ вас осталось '+ str(userPayment) +' минут, чтобы записать по нему видео'
            await bot.send_message(message.from_user.id, saluteText, reply_markup=loadvideo_kb)

class FSMLoadvid(StatesGroup):
    videoinfo = State()
# @dp.message_handler(commands=['загрузить видео'])
async def load_my_video(message : types.Message):
    tg_id = message.from_user.id
    usinfo = dbmain.checkIspolnByTgId(tg_id)
    if usinfo == 1:
        userPayment = dbmain.checkPaymentOfUser(tg_id)
        if userPayment == 1:
            checkVideoHave = dbmain.checkVideoHave(tg_id)
            if checkVideoHave == 1:
                successText = '''
                Ваше видео загружено\n\nПосле проверки модератором оно станет доступно членам жюри для оценки
                '''
                await bot.send_message(message.from_user.id, successText, reply_markup=loadedvideo_kb)
            else:
                await FSMLoadvid.videoinfo.set()
                await message.reply('Отправьте свой видео файл', reply_markup=cancel_kb)
        else:
            await bot.send_message(message.from_user.id, 'Нужно оплатить взнос.\n\n'\
            'Организационный взнос составляет 500 рублей за участие в одной номинации.', reply_markup=get_payment_kb)

# продолжение машинного состояния по ловле видеофайла, отправленного пользователем
# @dp.message_handler(content_types=['video'], state=FSMLoadvid.videoinfo)
async def load_video(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['video'] = message.video.file_id
        file = await bot.get_file(data['video'])
        file_path = file.file_path
        data['videoPath'] = "files/users-videos/" + data['video'] + ".mp4"
        await bot.download_file(file_path, data['videoPath'])
        print(file_path)
        data['usId'] = message.from_user.id
        # получаю отдельно текущую дату со временем, дату и время в разные переменные
        dateTimeReady_tmp = str(datetime.now()).split('.')
        dateTimeReady = dateTimeReady_tmp[0]
        dateTime_tmp = dateTimeReady.split(' ')
        dateOne = dateTime_tmp[0]
        timeOne = dateTime_tmp[1]
        data['loadDate'] = dateOne
        data['loadTime'] = timeOne
    await dbmain.updtVideoIdInUspayconvid(state)
    await state.finish()
    successText = '''
    Ваше видео загружено\n\nПосле проверки модератором оно станет доступно членам жюри для оценки
    '''
    await bot.send_message(message.from_user.id, successText, reply_markup=loadedvideo_kb)

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_register, Text(equals="зарегистрироваться", ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(get_firstname, state=FSMNewuser.firstname)
    dp.register_message_handler(get_lastname, state=FSMNewuser.lastname)
    dp.register_message_handler(get_patronymic, state=FSMNewuser.patronymic)
    dp.register_message_handler(get_birthDate, state=FSMNewuser.birthDate)
    dp.register_message_handler(get_kind, state=FSMNewuser.kind)
    dp.register_message_handler(get_phoneNumber, state=FSMNewuser.phoneNumber)
    dp.register_message_handler(get_vkLink, state=FSMNewuser.vkLink)
    dp.register_message_handler(get_education_institution, state=FSMNewuser.education_institution)
    dp.register_message_handler(get_teacher, state=FSMNewuser.teacher)
    dp.register_message_handler(cancel_handler, state="*", commands="отмена")
    dp.register_message_handler(edit_users_self_data, Text(equals="редактировать личные данные", ignore_case=True))
    dp.register_message_handler(send_rules_for_user, Text(equals="читать правила", ignore_case=True))
    dp.register_message_handler(apply_part, Text(equals="да! хочу участвовать!", ignore_case=True))
    dp.register_message_handler(get_poetry_text, Text(equals="получить текст номинации поэзия", ignore_case=True))
    dp.register_message_handler(get_poetry_text, Text(equals="получить текст номинации проза", ignore_case=True))
    dp.register_message_handler(get_poetry_text, Text(equals="получить текст номинации драматургия", ignore_case=True))
    dp.register_message_handler(load_my_video, Text(equals="загрузить видео", ignore_case=True))
    dp.register_message_handler(load_video, content_types=['video'], state=FSMLoadvid.videoinfo)
    dp.register_message_handler(get_new_user_data, state=FSMGotoeditusdata.updtdata)
    dp.register_message_handler(send_videoinstruction, Text(equals="согласен", ignore_case=True))
