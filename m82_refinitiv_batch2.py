#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3.1 CITADEL :: INJECTOR BATCH #2 (COMMODITIES & BLK)
# Molina Holdings | Sovereign Primary Edge L5
# ==============================================================================

import os, sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

NEW_EVENTS = [
    {
        "source": "MARITIME_ARAMCO",
        "headline": "Saudi Aramco headquarters attacked, limited fire reported as Houthis strike"
    },
    {
        "source": "ENERGY_DIESEL",
        "headline": "Global diesel shortages could persist well into 2027, IEA says"
    },
    {
        "source": "BLK_FINANCIALS",
        "headline": "BlackRock CEO Larry Fink says US interest rates will remain high long term"
    },
    {
        "source": "BLK_AI_RISK",
        "headline": "Larry Fink warns heavy data center construction debt could trigger US slowdown"
    }
]

def run_inject():
    if not os.path.exists(DB_PATH):
        print("❌ Error: DB no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")

    for ev in NEW_EVENTS:
        c.execute(
            "INSERT INTO m82_multi_stream (daemon_source, headline, status) VALUES (?, ?, 'PENDING');",
            (ev["source"], ev["headline"])
        )
        print(f"📥 [{ev['source']}] Inyectado -> {ev['headline'][:55]}...")

    conn.commit()
    conn.close()
    print("✅ Inyección de Lote #2 completada.")

if __name__ == "__main__":
    run_inject()
