import sqlite3

def init_db():
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            export_format TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def set_export_format(user_id, export_format):
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO user_settings (user_id, export_format) 
        VALUES (?, ?)
    ''', (user_id, export_format))
    conn.commit()
    conn.close()

def get_export_format(user_id):
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    c.execute('''
        SELECT export_format FROM user_settings WHERE user_id = ?
    ''', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 'txt'
