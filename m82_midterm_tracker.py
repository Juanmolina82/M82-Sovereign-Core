import sqlite3, datetime

DB_PATH = "/data/data/com.termux/files/home/M82/m82_database.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS m82_midterm_tracker (date TEXT PRIMARY KEY, wti REAL, rbob REAL, us10y REAL, spx REAL, gop_lead REAL, ipei REAL)')
c.execute('INSERT OR REPLACE INTO m82_midterm_tracker VALUES (?, 89.29, 3.27, 5.29, 5750.0, 2.8, 122.4)', (datetime.date.today().isoformat(),))
conn.commit()
conn.close()
print("✅ Tracker registrado en SQLite WAL.")
