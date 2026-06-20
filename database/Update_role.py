import sqlite3

connection = sqlite3.connect("cyberwatch.db")

cursor = connection.cursor()

cursor.execute("""
UPDATE users
SET role = 'admin'
WHERE id = 1
""")

connection.commit()

print("User role updated successfully")

connection.close()