import sqlite3

DATABASE_NAME = "user.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME, timeout=30)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserLink (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            uuid TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def insert_user_link(user_id, uuid):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO UserLink (user_id, uuid) VALUES (?, ?)', (user_id, uuid))
    conn.commit()
    conn.close()

def get_user_id_by_uuid(uuid):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM UserLink WHERE uuid = ?', (uuid,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None