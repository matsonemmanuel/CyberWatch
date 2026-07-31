import sqlite3

connection = sqlite3.connect("cyberwatch.db")

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
SELECT
    id,
    username,
    email,
    role,
    created_at
FROM users
ORDER BY id
""")

users = cursor.fetchall()

print("\n========== REGISTERED USERS ==========\n")

if not users:

    print("No users found.")

else:

    for user in users:

        print(dict(user))

connection.close()