#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def load_mobilization_signal():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()

    now = datetime.datetime.now().isoformat()
    headline = "VENEZUELA MOBILIZATION: Supporters of Maria Corina Machado mobilize across Venezuela demanding elections and safe return"
    source = "VENEZUELA_DESK"

    c.execute("""
        INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
        VALUES (?, ?, 'PENDING', ?)
    """, (source, headline, now))

    conn.commit()
    conn.close()
    print("✅ Evento de movilización inyectado correctamente en M82.")

if __name__ == "__main__":
    load_mobilization_signal()
