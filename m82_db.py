import sqlite3, os, time

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def get_connection(retries=10, delay=0.5):
    for attempt in range(retries):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=60.0)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=60000;")
            return conn
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < retries - 1:
                time.sleep(delay * (2 ** attempt))
            else:
                raise e

def execute_query(query, params=(), fetch=False):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    res = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return res
