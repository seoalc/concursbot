import pymysql.cursors
from datetime import datetime, timedelta
import re

############# проверка наличия исполнителя в базе по tg id ################
def checkIspolnByTgId (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful checkIspolnByTgId!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT firstname FROM users WHERE tg_id = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (tg_id))
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# проверка пользователя на оплату текущего конкурса ################
def checkPaymentOfUser (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful checkPaymentOfUser!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `id`, `user-id` FROM `payments` WHERE `user-id` = %s AND `videofileId` = 'empty'"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (tg_id))
            results = cursor.fetchone()
            if res == 1:
                # SQL
                sql2 = "SELECT `textTakingDate`, `textTakingTime` FROM `uspayconvid` WHERE `tg-id` = %s AND `videoId` = 'None'"
                # Выполнить команду запроса (Execute Query).
                # есть пользователь с этим ником в базе
                res2 = cursor.execute(sql2, (tg_id))
                results2 = cursor.fetchone()
                if results2['textTakingDate'] == '0000-00-00':
                    return 1
                else:
                    current_datetime = datetime.now()
                    # если месяц одинарный, добавляю ноль впереди
                    if len(str(current_datetime.month)) == 1:
                        monthNow = '0' + str(current_datetime.month)
                    else:
                        monthNow = str(current_datetime.month)
                    # текущая дата для выборки текущего времени из базы (за сегодня именно)
                    nowDate = str(current_datetime.year) + '-' + monthNow + '-' + str(current_datetime.day)
                    if nowDate == results2['textTakingDate']:
                        textTakingTimeStrp = datetime.strptime(results2['textTakingTime'], '%H:%M:%S')
                        nowTimeStr = str(current_datetime.hour) + ':' + str(current_datetime.minute) + ':' + str(current_datetime.second)
                        nowTimeStrp = datetime.strptime(nowTimeStr, '%H:%M:%S')
                        differenceTime = nowTimeStrp - textTakingTimeStrp
                        oneHour = timedelta(hours= 1 , minutes=00, seconds=00)
                        if differenceTime > oneHour:
                            return 0
                        else:
                            minutesKetti = str(differenceTime).split(':')
                            minutesLeft = 60 - int(minutesKetti[1])
                            return minutesLeft
                    else:
                        return 0
            else:
                return 0
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# проверка наличия текста у пользователя на час ################
def checkHavingText (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful checkHavingText!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `concurstextId` FROM `uspayconvid` WHERE `tg-id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (tg_id))
            results = cursor.fetchone()
            return results['concurstextId']
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# проверка наличия видео пользователя для текущего конкурса ################
def checkVideoHave (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful checkVideoHave!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `id` FROM videos WHERE `tg_id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (tg_id))
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# выбрать дату окончания текущих конкурсов ################
def getConcursesFinishDates ():
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful checkIspolnByTgId!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `finish-date` FROM concurses WHERE active = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (1))
            results = cursor.fetchone()
            return results['finish-date']
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# выбрать рандомный текст для пользователя по выбранной им номинации ################
def getRandomTextByNominationId (nominationId):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful getRandomTextByNominationId!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `id`, `nomination-id`, `name`, `text` FROM `concurstexts` WHERE `nomination-id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (nominationId))
            results = cursor.fetchall()
            return results
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

######## выбрать значение того параметра, который пользователь хочет отредактировать по названию #######
def getUsersDataByDataName (dataName, tg_id):
    if dataName == 'birthDate':
        dataName = 'birth-date'
    if dataName == 'vkLink':
        dataName = 'vk-link'
    if dataName == 'educationInstitution':
        dataName = 'education-institution'
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful getUsersDataByDataName!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `" + dataName + "` FROM `users` WHERE `tg_id` = %s"
            # Выполнить команду запроса (Execute Query).
            # выбрать значение по названию колонки
            res = cursor.execute(sql, (tg_id))
            results = cursor.fetchone()
            return results
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# проверка статуса пользователя, оплатил ли, получил ли текст ################
def checkUserStatus (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful getRandomTextByNominationId!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `id` FROM `uspayconvid` WHERE `tg_id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (tg_id))
            if res == 1:
                usId = 3
            else:
                usId = 2
            return usId
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# выбрать состояния пользователя (оплачен ли, принят ли текст, оплачен ли текст) ################
def checkPaymentStatus (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful checkIspolnByTgId!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `paymentStatus` FROM `users` WHERE `tg_id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (tg_id))
            results = cursor.fetchone()
            return results['paymentStatus']
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# запись нового пользователя в базу ################
async def addNewUser (state):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful addNewUser!")
    cursor = connection.cursor()
    try:
        async with state.proxy() as data:
            # SQL
            sql = "INSERT INTO `users` "\
            "(`tg_id`, `username`, `firstname`, `lastname`, `patronymic`, `birth-date`, `age`, `kind`, `users-category`, `phone`, `vk-link`, `education-institution`, `teacher`) "\
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, tuple(data.values()))
            connection.commit()
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# запись информации о новом платеже в базу ################
async def addNewPayment (usId, concursId, dateTimeReady, dateOne, timeOne):
    # передаваемые в функцию переменные перевожу в ловарь для вставки в базу кортежем
    a = {'usId': usId, 'concursId': concursId, 'dateTimeReady': dateTimeReady, 'dateOne': dateOne, 'timeOne': timeOne}

    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful addNewPayment!")
    cursor = connection.cursor()
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "INSERT INTO `payments` "\
            "(`user-id`, `concurs-id`, `date`, `chislo`, `vremya`) "\
            "VALUES (%s, %s, %s, %s, %s)"
            # Выполнить команду запроса (Execute Query).
            # перевожу данные в кортеж для вставки
            res = cursor.execute(sql, tuple(a.values()))
            # и сразу после вставки информации о платеже в базу
            # вставляю id пользователя, конкурса и только что вставленного платежа
            # в связывающую таблицу uspayconvid
            lastId = connection.insert_id()
            b = {'usId': usId, 'concursId': concursId, 'lastId': lastId}
            sql2 = "INSERT INTO `uspayconvid` "\
            "(`tg-id`, `concursId`, `paymentId`) "\
            "VALUES (%s, %s, %s)"
            res2 = cursor.execute(sql2, tuple(b.values()))

            # обнавления статуса о платеже для этого пользователя в таблице usersDataByDataName
            sql3 = "UPDATE `users` SET "\
            "`paymentStatus` = 1 WHERE `tg_id` = %s"
            res3 = cursor.execute(sql3, (usId))
            connection.commit()

            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# обновление информации о новом платеже в связывающей таблице uspayconvid ################
############# функция срабатывает во время отправки текста пользователю #############
async def updtUspayconvid (tg_id, textId, nominationId, dateOne, timeOne):
    # передаваемые в функцию переменные перевожу в ловарь для вставки в базу кортежем
    a = {'concurtextId': textId, 'nominationId': nominationId, 'dateOne': dateOne, 'timeOne': timeOne, 'usId': tg_id}

    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful addNewPayment!")
    cursor = connection.cursor()
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "UPDATE `uspayconvid` SET "\
            "`concurstextId` = %s, `nominationId` = %s, `textTakingDate` = %s, `textTakingTime` = %s WHERE `tg-id` = %s"
            # Выполнить команду запроса (Execute Query).
            # перевожу данные в кортеж для вставки
            res = cursor.execute(sql, tuple(a.values()))
            connection.commit()
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

######## обновление информации о загруженном видео в связывающей таблице uspayconvid ############
############# функция срабатывает во время загрузки видео #############
async def updtVideoIdInUspayconvid (state):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful updtVideoIdInUspayconvid!")
    cursor = connection.cursor()
    try:
        async with state.proxy() as data:
            a = {'fileId': data['video'], 'usId': data['usId']}
            # SQL
            sql = "UPDATE `uspayconvid` SET "\
            "`videoId` = %s WHERE `tg-id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, tuple(a.values()))

            c = {'usId': data['usId'], 'fileId': data['video']}
            # SQL
            sql3 = "SELECT `concurstextId`, `nominationId` FROM `uspayconvid` WHERE `tg-id` = %s AND `videoId` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res3 = cursor.execute(sql3, tuple(c.values()))
            results = cursor.fetchone()

            b = {'usId': data['usId'], 'loadDate': data['loadDate'], 'loadTime': data['loadTime'], 'fileId': data['video'], 'concurstextId': results['concurstextId'], 'nominationId': results['nominationId'], 'filePath': data['videoPath']}
            sql2 = "INSERT INTO `videos` "\
            "(`tg_id`, `loadDate`, `loadTime`, `fileId`, `concurstextId`, `nominationId`, `filePath`) "\
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            res2 = cursor.execute(sql2, tuple(b.values()))
            connection.commit()
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# обновление личных данных пользователя при редактировании им ################
async def updtUsersInfo (state):

    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful updtUsersInfo!")
    cursor = connection.cursor()
    try:
        async with state.proxy() as data:
            dateFind = re.findall("(\d{2}-\d{2}-\d{4})", str(data['userData']))
            if len(dateFind) == 1:
                # для работы со строкой как типом datetime ее привожу к этому типу
                birth_date = datetime.strptime(data['userData'], '%d-%m-%Y')
                # для заноса даты в таблицу MySQL необходимо вернуть ее к формату ГГГГ-ММ-ДД
                birth_date = datetime.strftime(birth_date, '%d-%m-%Y')
                birth_date_tmp = str(birth_date).split('-')
                birth_date_new = birth_date_tmp[2] + '-' + birth_date_tmp[1] + '-' + birth_date_tmp[0]
                data['userData'] = birth_date_new
            a = {'userData': data['userData'], 'tg-id': data['tg-id']}
            # SQL
            sql = "UPDATE `users` SET "\
            "`" + data['dataName'] + "` = %s WHERE `tg_id` = %s"
            # Выполнить команду запроса (Execute Query).
            # перевожу данные в кортеж для вставки
            res = cursor.execute(sql, tuple(a.values()))
            connection.commit()
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()
