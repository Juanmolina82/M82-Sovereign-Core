#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3.1 CITADEL :: INJECTOR (BLACKROCK Q3 2026 EARNINGS)
# Molina Holdings | Sovereign Primary Edge L5
# ==============================================================================

import os, sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

EVENT = {
    "source": "BLK_Q3_EARNINGS",
    "headline": "BlackRock Q3 2026 EPS $15.93 (+38%), AUM hits record $15.5T with $205B net inflows"
}

def inject():
    if not os.path.exists(DB_PATH):
        print("❌ Error: DB no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    c.execute(
        "INSERT INTO m82_multi_stream (daemon_source, headline, status) VALUES (?, ?, 'PENDING');",
        (EVENT["source"], EVENT["headline"])
    )
    conn.commit()
    conn.close()
    print(f"📥 [{EVENT['source']}] Inyectado: {EVENT['headline']}")

if __name__ == "__main__":
    inject()
