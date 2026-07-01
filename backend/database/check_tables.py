import sqlite3

connection = sqlite3.connect('cyberwatch.db')

cursor = connection.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

tables = cursor.fetchall()

for table in tables:
    print(table)

connection.close()