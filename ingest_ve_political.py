#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def load_ve_signal():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()

    now = datetime.datetime.now().isoformat()
    headline = "VENEZUELA GEOPOLITICS: Jefa de comunicaciones de Maria Corina Machado regresa a Venezuela tras año y medio de exilio"
    source = "VENEZUELA_DESK"

    c.execute("""
        INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
        VALUES (?, ?, 'PENDING', ?)
    """, (source, headline, now))

    conn.commit()
    conn.close()
    print("✅ Alerta política de Venezuela inyectada exitosamente en la cola M82.")

if __name__ == "__main__":
    load_ve_signal()
