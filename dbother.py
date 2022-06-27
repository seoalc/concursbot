import pymysql.cursors

############# выбрать tg-id всех пользователей кто зарегался и не оплатил ################
def getAllNotpayUsersTGID ():
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful getAllUsersTGID!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `tg_id` FROM `users` WHERE `paymentStatus` = 0"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql)
            results = cursor.fetchall()
            return results
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# выбрать tg-id всех пользователей кто зарегался и не оплатил ################
def getallNotvideosUsersTGID ():
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful getallNotvideosUsersTGID!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `tg-id` FROM `uspayconvid` WHERE `videoId` = 'None'"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql)
            results = cursor.fetchall()
            return results
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# выбрать tg-id всех пользователей кто зарегался и не оплатил ################
def getTimesForNowDate (nowDate):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful getTimesForNowDate!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `tg-id`, `textTakingTime` FROM `uspayconvid` WHERE `textTakingDate` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (nowDate))
            results = cursor.fetchall()
            return results
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# обнуление информации о платеже в таблице users ################
############# функция срабатывает во время неотправки видео в течение часа #############
async def resetPaymentStatusForUser (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful resetPaymentStatusForUser!")
    cursor = connection.cursor()
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "UPDATE `users` SET "\
            "`paymentStatus` = 0 WHERE `tg-id` = %s"
            # Выполнить команду запроса (Execute Query).
            # перевожу данные в кортеж для вставки
            res = cursor.execute(sql, (tg_id))
            connection.commit()
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()
