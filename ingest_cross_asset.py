#!/usr/bin/env python3
import sqlite3, os, datetime

DB = os.path.expanduser("~/M82/m82_database.db")

headline = "M82_WIRE CROSS-ASSET: Global Red Sweep in Equities • US 10Y Yields Surge • Energy Volatility"
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

conn = sqlite3.connect(DB, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
c = conn.cursor()

c.execute("""
    INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES ('M82_WIRE_CROSS_ASSET', ?, 'PENDING', ?)
""", (f"{headline} [{now}]", now))

conn.commit()
conn.close()
print("✅ Señal Cross-Asset inyectada a m82_database.db. El daemon procesará la tarjeta HD.")
