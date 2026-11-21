#!/usr/bin/env python3
import sqlite3, os, datetime

DB = os.path.expanduser("~/M82/m82_database.db")

headline = "GLOBAL BONDS: Broad Sell-Off in Sovereign Debt - Yield Pressure Escalates Risk-Off Sentiment"
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

conn = sqlite3.connect(DB, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
c = conn.cursor()

c.execute("""
    INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES ('M82_WIRE_BONDS', ?, 'PENDING', ?)
""", (f"{headline} [{now}]", now))

conn.commit()
conn.close()
print("✅ Evento de Mercado de Bonos inyectado. El daemon procesará la señal a tarjeta HD.")
