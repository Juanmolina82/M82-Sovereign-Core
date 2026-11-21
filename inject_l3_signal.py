#!/usr/bin/env python3
import sqlite3, os, time

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def inject_signal():
    headline = "ARBITRAGE ALERT: Brent Physical $106.14 + Dubai Physical $119.28 vs Venezuela Pact Price $64.63 | Net Loss: -$54.65/bbl ($8.0B/yr)"
    source = "M82_ARBITRAGE_L3"

    for attempt in range(5):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=30.0)
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("""
                INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status)
                VALUES (?, ?, 'PENDING')
            """, (source, headline))
            conn.commit()
            conn.close()
            print(f"✅ Señal L3 inyectada con éxito: {headline[:70]}...")
            break
        except sqlite3.OperationalError:
            print("⏳ DB ocupada, reintentando en 1 segundo...")
            time.sleep(1)

if __name__ == "__main__":
    inject_signal()
