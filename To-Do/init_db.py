import sqlite3

conn=sqlite3.connect("users.db")
cursor=conn.cursor()

#users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
    )
    """)

#task table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    description TEXT,
    start TEXT,
    end TEXT,
    status TEXT DEFAULT 'pending',
    priority TEXT DEFAULT 'medium', user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
    )
""")
conn.commit()
conn.close()
print("DB initialized")