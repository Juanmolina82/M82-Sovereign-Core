#!/usr/bin/env python3
import sqlite3, os, datetime

DB = os.path.expanduser("~/M82/m82_database.db")

headline = "M82_WIRE OIL & COMMODITIES: Saudi Resumes Yanbu Loadings • Asia OSP Hikes Planned • Middle East Supply Shifts"
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

conn = sqlite3.connect(DB, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
c = conn.cursor()

c.execute("""
    INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES ('M82_WIRE_COMMODITIES', ?, 'PENDING', ?)
""", (f"{headline} [{now}]", now))

conn.commit()
conn.close()
print("✅ Señal Geopolítica de Petróleo inyectada a m82_database.db.")
