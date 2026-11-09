#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3.1 CITADEL :: INJECTOR (TESLA $30B SEC CREDIT FILING)
# Primary Sovereign Edge Node L5
# ==============================================================================

import os, sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

EVENTS = [
    {
        "source": "REFINITIV_TECH",
        "headline": "Tesla locks $30B credit Citi/Wells ($20B term + $10B revolver). Capex guide >$25B vs $8.5B 25 for AI clusters, Terafab SpaceX and Cybercab/Optimus."
    },
    {
        "source": "REFINITIV_TECH",
        "headline": "Tesla $43B cash but draws $30B line as capex 3x. Insurance against semi crunch, power demand and Terafab $16.8B expansion."
    }
]

def inject():
    if not os.path.exists(DB_PATH):
        print("❌ Error: DB no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    
    for ev in EVENTS:
        c.execute(
            "INSERT INTO m82_multi_stream (daemon_source, headline, status) VALUES (?, ?, 'PENDING');",
            (ev["source"], ev["headline"])
        )
        print(f"📥 [{ev['source']}] Inyectado -> {ev['headline'][:60]}...")

    conn.commit()
    conn.close()
    print("✅ Inyección de eventos Tesla $30B completada.")

if __name__ == "__main__":
    inject()
