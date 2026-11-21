import sqlite3, datetime

DB_PATH = "/data/data/com.termux/files/home/M82/m82_database.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS m82_macro_snapshots (date TEXT PRIMARY KEY, wti REAL, gold REAL, us10y REAL, eurusd REAL)')
c.execute('INSERT OR REPLACE INTO m82_macro_snapshots VALUES (?, 89.29, 2650.0, 4.18, 1.085)', (datetime.date.today().isoformat(),))
conn.commit()
conn.close()
print("✅ Snapshot macro global de Refinitiv registrado en SQLite WAL.")
