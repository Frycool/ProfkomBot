import sqlite3 as sql

def create_table():
    # Создание таблицы внутри базы данных
    connection = sql.connect('Database')
    cursor =  connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id REAL PRIMARY KEY,
    message_thread_id REAL INTEGER
    )
    ''')
    connection.commit()
    connection.close()



def find_group_id(user_id):
    connection = sql.connect('DataBase')  # Подключение к базе данных
    cursor = connection.cursor()

    cursor.execute('''SELECT message_thread_id FROM Users WHERE id = ?''', (user_id,))

    message_tread_id = cursor.fetchone()

    connection.close()

    return message_tread_id

def check_user_id(user_id):
    connection = sql.connect('DataBase')  # Подключение к базе данных
    cursor = connection.cursor()

    cursor.execute('''SELECT id FROM Users WHERE id = ?''', (user_id,))

    user = cursor.fetchone()
    connection.close()

    if user:
        return True
    else:
        return False
