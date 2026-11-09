#!/usr/bin/env python3
import sqlite3, os, datetime

DB = os.path.expanduser("~/M82/m82_database.db")

headline_macro = "GLOBAL MARKets: US 10Y Yields >5% • Strong Dollar Hits LatAm • High Rates Regime"
headline_comm  = "ENERGY & COMMODITIES: Saudi Raises Asia OSP • Yanbu Restart • Middle East Supply Shifts"
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

conn = sqlite3.connect(DB, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
c = conn.cursor()

c.execute("""
    INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES ('M82_WIRE_GLOBAL_MARKETS', ?, 'PENDING', ?)
""", (f"{headline_macro} [{now}]", now))

c.execute("""
    INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES ('M82_WIRE_COMMODITIES', ?, 'PENDING', ?)
""", (f"{headline_comm} [{now}]", now))

conn.commit()
conn.close()
print("✅ Señales Macro y Commodities inyectadas a m82_database.db.")
