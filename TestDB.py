import psycopg2
import urllib.parse as up
up.uses_netloc.append("postgres")

path_to_db_bot = 'postgres://khxkqmir:HUILxSAV3nXHrlwtSSrY-Ep3F_KmJhxk@rajje.db.elephantsql.com/khxkqmir'
url = up.urlparse(path_to_db_bot)

connection = psycopg2.connect(database=url.path[1:],

                              user=url.username,

                              password=url.password,

                              host=url.hostname,

                              port=url.port)
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS shop(name TEXT, price INTEGER, rating REAL)')
connection.commit()
cursor.execute('SELECT * FROM shop')
data = cursor.fetchall()
print(data)
# cursor.execute('INSERT INTO shop VALUES(%s, %s, %s)', ('когтеточка', '15000', '9.3'))
# connection.commit()

