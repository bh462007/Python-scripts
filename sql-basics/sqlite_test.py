import sqlite3

connection=sqlite3.connect("reconciliation.db")

cursor=connection.cursor()

cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS invoices (
        invoice_id TEXT PRIMARY KEY,
        vendor TEXT,
        amount REAL,
        date TEXT
    )
    """)

connection.commit()

cursor.execute("DELETE FROM invoices")
connection.commit()


cursor.execute("""
    INSERT INTO invoices (invoice_id, vendor, amount, date)
    VALUES (?, ?, ?, ?)
""", ("INV001", "abc ltd", 5000, "2026-09-20"))

connection.commit()

cursor.execute("SELECT * FROM invoices")
rows=cursor.fetchall()

for row in rows:
    print(row)

cursor.execute(
    "UPDATE invoices SET amount = ? WHERE invoice_id = ?",
    (5500, "INV001")
)

connection.commit()

cursor.execute(
    "SELECT * FROM invoices WHERE invoice_id = ?",
    ("INV001",)
)

row = cursor.fetchone()

print(row)

cursor.execute(
    "DELETE FROM invoices WHERE invoice_id = ?",
    ("INV001",)
)

connection.commit()

cursor.execute("SELECT * FROM invoices")

rows = cursor.fetchall()

print(rows)

connection.close()