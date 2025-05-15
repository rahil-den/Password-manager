import sqlite3

DB_FILE = 'passwords.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_entry(site, username, encrypted_password):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)",
                       (site, username, encrypted_password))
        conn.commit()

def get_entries():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM passwords")
        return cursor.fetchall()

def get_entries_by_site(site):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM passwords WHERE site=?", (site,))
        return cursor.fetchall()

def delete_entry(site):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM passwords WHERE site = ?", (site,))
        conn.commit()


def list_all_sites():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT site FROM passwords")
        return [row[0] for row in cursor.fetchall()]



