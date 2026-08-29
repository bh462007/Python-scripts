import sqlite3

conn=sqlite3.connect("users.db")
cursor=conn.cursor()

cursor.execute("select * from users")

print(cursor.fetchall())

conn.close()