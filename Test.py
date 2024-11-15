import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()

import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Добавляем нового пользователя
cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', ('newuser', 'newuser@example.com', 28))

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()

import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем имена и возраст пользователей старше 25 лет
cursor.execute('SELECT username, age FROM Users WHERE age > ?', (25,))
results = cursor.fetchall()

for row in results:
  print(row)

connection.close()