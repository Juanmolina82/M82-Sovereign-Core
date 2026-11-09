import sqlite3, os, time

DB = os.path.expanduser("~/M82/m82_database.db")

def checkpoint_wal():
    while True:
        try:
            conn = sqlite3.connect(DB, timeout=30.0)
            conn.execute("PRAGMA wal_checkpoint(PASSIVE);")
            conn.close()
        except Exception as e:
            pass
        time.sleep(60)

if __name__ == "__main__":
    checkpoint_wal()
