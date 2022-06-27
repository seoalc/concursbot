import pymysql.cursors

############# проверка наличия исполнителя в членах жюри по tg id ################
def checkJuryByTgId (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='pass',
                                 db='concurs-testbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful checkJuryByTgId!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `id` FROM `jury` WHERE `tg-id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (tg_id))
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# выбрать новые видео, которым еще не выставлял оценку ################
def getAllNewVideos (tg_id, nominationId):
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
            # SQL выбираю из базы сначала видео за которые он уже проголосовал
            sql4 = "SELECT `videoPrimary` FROM `vidjurylink` WHERE `juryId` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res4 = cursor.execute(sql4, (tg_id))
            results4 = cursor.fetchall()

            if len(results4) == 0:
                # SQL
                sql = "SELECT * FROM `videos` WHERE status = 1 AND `nominationId` = %s"
                # Выполнить команду запроса (Execute Query).
                # есть пользователь с этим ником в базе
                res = cursor.execute(sql, (nominationId))
                sloiv = cursor.fetchall()
            else:
                # создаю пустой список, делаю выборку тех только видео, за которые он еще не проголосовал
                # добавляю их в него
                sloiv = []
                i = 0
                for element4 in results4:
                    c = {'nominationId': nominationId, 'id': element4['videoPrimary']}
                    # SQL
                    sql5 = "SELECT * FROM `videos` WHERE status = 1 AND `nominationId` = %s AND `id` != %s"
                    # Выполнить команду запроса (Execute Query).
                    # есть пользователь с этим ником в базе
                    res5 = cursor.execute(sql5, tuple(c.values()))
                    results5 = cursor.fetchone()
                    # sloiv['slov' + str(i)] = results5
                    sloiv.append(results5)
                    i += 1

            # SQL выборка названия номинации
            sql2 = "SELECT `name` FROM `nominations` WHERE `id` = %s"
            # Выбираю номинацию из таблицы с номинациями по id
            res2 = cursor.execute(sql2, (nominationId))
            results2 = cursor.fetchone()

            # в получившийся список кортежей на каждой итерации цикла добавляю еще поля
            for element in sloiv:
                # SQL выборка названия текста
                sql3 = "SELECT `name` FROM `concurstexts` WHERE `id` = %s"
                # Выбираю номинацию из таблицы с номинациями по id
                res3 = cursor.execute(sql3, (element['concurstextId']))
                results3 = cursor.fetchone()
                element['nominationName'] = results2['name']
                element['textName'] = results3['name']
            return sloiv
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# запись нового голоса для конкретного видео ################
async def sendVoiceFor (voice, videoId, juryID):
    # передаваемые в функцию переменные перевожу в ловарь для вставки в базу кортежем
    a = {'videoPrimary': videoId, 'juryId': juryID, 'score': voice}

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
            sql = "INSERT INTO `vidjurylink` "\
            "(`videoPrimary`, `juryId`, `score`) "\
            "VALUES (%s, %s, %s)"
            # Выполнить команду запроса (Execute Query).
            # перевожу данные в кортеж для вставки
            res = cursor.execute(sql, tuple(a.values()))
            connection.commit()

            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()
