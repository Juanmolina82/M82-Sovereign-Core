#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3.1 CITADEL :: INJECTOR (LPL FINANCIAL PROFILE & ALLIANCE)
# Primary Sovereign Edge Node L5
# ==============================================================================

import os, sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

EVENT = {
    "source": "REFINITIV_BANKING",
    "headline": "LPL Financial LLC profile loaded: $818.3B total assets, $10.76B revenue. Strategic M82 alliance proposal initialized."
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
    print(f"📥 [{EVENT['source']}] Inyectado -> {EVENT['headline'][:65]}...")

if __name__ == "__main__":
    inject()
