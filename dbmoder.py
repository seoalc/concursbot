import pymysql.cursors

############# проверка наличия исполнителя в членах жюри по tg id ################
def checkModerByTgId (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful checkModerByTgId!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `id` FROM `moders` WHERE `tg-id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (tg_id))
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# получить для модератора видео, которые неодобренные ################
def getNotApprovedVideos ():
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful getNotApprovedVideos!")
    try:
        with connection.cursor() as cursor:
            # SQL выбираю из базы сначала видео за которые он уже проголосовал
            sql = "SELECT * FROM `videos` WHERE `status` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (0))
            results = cursor.fetchall()
            for element in results:
                # SQL выборка названия номинации
                sql2 = "SELECT `name` FROM `nominations` WHERE `id` = %s"
                # Выбираю номинацию из таблицы с номинациями по id
                res2 = cursor.execute(sql2, (element['nominationId']))
                results2 = cursor.fetchone()
                # SQL выборка названия текста
                sql3 = "SELECT `name` FROM `concurstexts` WHERE `id` = %s"
                # Выбираю номинацию из таблицы с номинациями по id
                res3 = cursor.execute(sql3, (element['concurstextId']))
                results3 = cursor.fetchone()
                element['nominationName'] = results2['name']
                element['concurstextName'] = results3['name']
            return results
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# обновление статуса видео на одобренное ################
async def setApproveStatus (videoId):
    # передаваемые в функцию переменные перевожу в ловарь для вставки в базу кортежем
    a = {'status': 1, 'videoId': videoId}

    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful setApproveStatus!")
    cursor = connection.cursor()
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "UPDATE `videos` SET "\
            "`status` = %s WHERE id = %s"
            # Выполнить команду запроса (Execute Query).
            # перевожу данные в кортеж для вставки
            res = cursor.execute(sql, tuple(a.values()))
            connection.commit()
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()
