import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn
