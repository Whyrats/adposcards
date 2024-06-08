import sqlite3

def init_db():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
                    user_id INTEGER PRIMARY KEY,
                    export_format TEXT DEFAULT 'txt'
                )''')
    conn.commit()
    conn.close()

def set_export_format(user_id, export_format):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO settings (user_id, export_format) VALUES (?, ?)', (user_id, export_format))
    conn.commit()
    conn.close()

def get_export_format(user_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('SELECT export_format FROM settings WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 'txt'
