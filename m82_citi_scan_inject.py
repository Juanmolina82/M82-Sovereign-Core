#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3.2 CITADEL :: CITIGROUP INC. (C) REFINITIV INJECTOR
# Venue: Caracas HQ Master Node | Molina Holdings LLC / Corp. Intl JMM, C.A.
# ==============================================================================

import os, sqlite3, hashlib

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

RAW_TELEMETRY = [
    ("BANKING", "Citigroup Inc (C) Market Cap $103.5B / Rev $81.1B — ESG Score 43.11 (Env 94.6, Gov 90.0) — Refinitiv Workspace", "US MegaCap Banking", 0.94),
    ("BANKING", "Wall Street Peers Benchmarking: MS Cap $244B vs GS Cap $239B vs C Cap $103B — Alpha Model Score 71 Bullish", "Investment Banking Basket", 0.96)
]

def inject_citi():
    if not os.path.exists(DB_PATH):
        print("❌ DB no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    c.execute("PRAGMA journal_mode=WAL;")

    inserted = 0
    for desk, headline, tag, alpha in RAW_TELEMETRY:
        clean_hl = f"[{desk} | Caracas HQ] {headline}"[:115]
        h_hash = hashlib.sha256(clean_hl.encode()).hexdigest()[:16]

        try:
            c.execute("""
                INSERT INTO m82_multi_stream 
                (daemon_source, headline, headline_hash, desk, status, alpha_score, asset_impact, created_at)
                VALUES (?, ?, ?, ?, 'VERIFIED', ?, 'REFINITIV_CITI_SCAN', CURRENT_TIMESTAMP)
            """, (desk, clean_hl, h_hash, tag, alpha))
            inserted += 1
            print(f"📥 [{desk}] {clean_hl[:65]}... (VERIFIED)")
        except sqlite3.IntegrityError:
            print(f"⚠️ DUPE SKIPPED: {clean_hl[:45]}...")

    conn.commit()
    conn.close()
    print(f"\n✅ Inyección Citigroup completada: {inserted} eventos procesados.")

if __name__ == "__main__":
    inject_citi()
