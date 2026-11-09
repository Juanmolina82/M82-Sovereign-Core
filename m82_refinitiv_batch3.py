#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3.1 CITADEL :: INJECTOR BATCH #3 (WSJ / REFINITIV FEEDS)
# Molina Holdings | Sovereign Primary Edge L5
# ==============================================================================

import os, sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

EVENTS = [
    {
        "source": "REFINITIV_MARITIME",
        "headline": "Two cargo ships sunk near Strait of Hormuz as Iranian attacks increase on shipping lanes"
    },
    {
        "source": "REFINITIV_GEOPOL",
        "headline": "Ukraine says new limits on Starlink are disrupting its military and drone operations"
    },
    {
        "source": "REFINITIV_BANKING",
        "headline": "Wall Street worries Bank of America trading weakness and $1.2B charge problems will linger"
    },
    {
        "source": "REFINITIV_MACRO",
        "headline": "US $1.7 trillion auto loan market heads for crash as monthly payments average $750"
    },
    {
        "source": "REFINITIV_TECH",
        "headline": "Eight US states sue OpenAI claiming ChatGPT causes harm to children"
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
    print("✅ Inyección de Lote #3 completada.")

if __name__ == "__main__":
    inject()
