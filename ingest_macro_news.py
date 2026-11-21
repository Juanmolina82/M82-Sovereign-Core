#!/usr/bin/env python3
import sqlite3, os, datetime

DB = os.path.expanduser("~/M82/m82_database.db")

headline = "US MACRO: S&P 500 flat as 10Y Yields hit 5.078% - Energy Inflation pressures Fed"
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

conn = sqlite3.connect(DB, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
c = conn.cursor()

c.execute("""
    INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES ('M82_WIRE_MACRO_NEWS', ?, 'PENDING', ?)
""", (f"{headline} [{now}]", now))

conn.commit()
conn.close()
print("✅ Alerta Macro inyectada a m82_database.db. El daemon generará la tarjeta HD.")
