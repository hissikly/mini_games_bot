import sqlite3

conn = sqlite3.connect('s.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users(name TEXT, surname TEXT, age INT)')
cursor.execute('INSERT INTO users(name, surname, age) VALUES("Mark", "Tven", 40)')
# cursor.execute('INSERT INTO users(id, username, num) VALUES(?, ?, ?)', (us_id, us, us_num))
conn.commit()
# cursor.execute('SELECT name FROM users WHERE age = ?', (20,))
data = cursor.fetchall()
print(data)
