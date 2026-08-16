import sqlite3

DB_NAME = "urls.db"


def get_connection():
    return sqlite3.connect(DB_NAME)

def create_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

create_database()
