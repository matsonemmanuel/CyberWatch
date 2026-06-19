
import os

print("Database:", os.path.abspath("cyberwatch.db"))

import sqlite3

connection = sqlite3.connect('cyberwatch.db')

cursor = connection.cursor()

cursor.execute("SELECT * FROM users")

rows = cursor.fetchall()

print("Total Users:", len(rows))

for row in rows:
    print(row)

connection.close()