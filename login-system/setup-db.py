import sqlite3

conn=sqlite3.connect("users.db")
cursor=conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(id integer primary key AUTOINCREMENT, username text unique not null , password_hash text not null)""")

conn.commit()
conn.close()
print("DB setup completed")