import sqlite3 as sql

def create_table():
    # Создание таблицы внутри базы данных
    connection = sql.connect('Database')
    cursor =  connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    message_thread_id INTEGER,
    act INTEGER,
    fio INTEGER,
    admin INTEGER
    )
    ''')
    connection.commit()
    connection.close()

def create_new_user(user_id): # Просто создание связи между человек и группой
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO Users (id, message_thread_id, act, fio, admin) VALUES (?, ?, ?, ?, ?)''', (user_id, 42, 1, 0, 0,))

    connection.commit()
    connection.close()

def create_admins_list(admin_ids):
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''SELECT id FROM Users WHERE admin = ?''', (1,))

    admins = cursor.fetchall()
    connection.close()

    for id in admins:
        admin_ids.append(id)



def make_admin(user_id):
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''UPDATE Users SET admin = ? WHERE id = ?''', (1 ,user_id,))


    connection.commit()
    connection.close()

def delete_admin(user_id,admin_ids):
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''UPDATE Users SET admin = ? WHERE id = ?''', (0 ,user_id,))

    connection.commit()
    connection.close()

    admin_ids.remove(user_id)

def change_fio(user_id):
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''UPDATE Users SET fio = ? WHERE id = ?''', (1 ,user_id,))

    connection.commit()
    connection.close()


def change_message_thread_id(user_id,message_thread_id):
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''UPDATE Users SET message_thread_id = ? WHERE id = ?''', (message_thread_id, user_id,))

    connection.commit()
    connection.close()

def find_fio(user_id): # Эта часть кода првоверяет, ФИО вписано пользователем или нет
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''SELECT fio FROM Users WHERE id = ?''', (user_id,))

    fio = cursor.fetchone()[0]
    connection.close()

    return fio

def find_act(user_id): # Эта часть кода првоверяет, ФИО вписано пользователем или нет
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''SELECT act FROM Users WHERE id = ?''', (user_id,))

    act = cursor.fetchone()[0]

    connection.close()

    return act

def change_act(user_id):
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''SELECT act FROM Users WHERE id = ?''', (user_id,))

    act = cursor.fetchone()[0]

    if act == 0:
        cursor.execute('''UPDATE Users SET act = ? WHERE id = ?''', (1,user_id,))
    else:
        cursor.execute('''UPDATE Users SET act = ? WHERE id = ?''', (0, user_id,))

    connection.commit()
    connection.close()

def find_group_id(user_id):
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''SELECT message_thread_id FROM Users WHERE id = ?''', (user_id,))

    message_tread_id = cursor.fetchone()[0]

    connection.close()

    return message_tread_id

def check_user_id(user_id):
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''SELECT id FROM Users WHERE id = ?''', (user_id,))

    user = cursor.fetchone()
    connection.close()

    if user:
        return True
    else:
        return False

def find_chat_id(message_thread_id):
    connection = sql.connect('DataBase')
    cursor = connection.cursor()

    cursor.execute('''SELECT id FROM Users WHERE message_thread_id = ?''', (message_thread_id,))

    user_id = cursor.fetchone()[0]

    connection.close()

    return user_id
