import sqlite3
import os


# Database Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    '..',
    'database',
    'cyberwatch.db'
)

print("Database Path:", DATABASE_PATH)

def get_db_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection