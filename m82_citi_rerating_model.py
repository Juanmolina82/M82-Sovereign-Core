#!/usr/bin/env python3
# ==============================================================================
# M82 V60.4.2 CITADEL :: CITI P/B RE-RATING MODEL & LPL DECK INJECTOR (D-51)
# Venue: Caracas HQ Master Node | Molina Holdings LLC / Corp. Intl JMM C.A.
# ==============================================================================

import os, sqlite3, hashlib

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Parametrización del Modelo de Re-Rating
CITI_MARKET_CAP_CURRENT = 103.55  # $B
CITI_PB_CURRENT = 0.61
CITI_PB_TARGET = 0.90
UPSIDE_PCT = round(((CITI_PB_TARGET - CITI_PB_CURRENT) / CITI_PB_CURRENT) * 100, 2)
CITI_TARGET_CAP = round(CITI_MARKET_CAP_CURRENT * (1 + UPSIDE_PCT/100), 2)

RERATING_DATA = [
    ("EQUITIES", f"Citi (C.N) P/B Re-Rating Model: 0.61x -> 0.90x Target | Market Cap ${CITI_MARKET_CAP_CURRENT}B -> ${CITI_TARGET_CAP}B (+{UPSIDE_PCT}%)", "CITI_RERATE_MODEL", 0.99),
    ("EQUITIES", f"LPL Institutional Deck: Citi Real ESG 85.19 #1 vs Combined 43.11 (Controversies Drag 1.02) — High Alpha Arbitrage", "LPL_PITCH_DECK", 0.98),
    ("TREASURY", f"LPL Compliance (LPLA.OQ): 63.58 ESG Clean Base — D-33 Risk Gate & D-34 Zero-PII Bridge Validated", "LPL_COMPLIANCE", 0.97)
]

def run_citi_rerating_model():
    if not os.path.exists(DB_PATH):
        print("❌ DB no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA busy_timeout=60000;")

    ins = 0
    for desk, hl, tag, alpha in RERATING_DATA:
        clean_hl = f"[{desk}] {hl}"[:120]
        h_hash = hashlib.sha256(clean_hl.encode()).hexdigest()[:16]

        try:
            c.execute("""
                INSERT INTO m82_multi_stream 
                (daemon_source, headline, headline_hash, desk, status, alpha_score, asset_impact, created_at)
                VALUES (?, ?, ?, ?, 'VERIFIED', ?, 'CITI_RERATING_V6042', CURRENT_TIMESTAMP)
            """, (desk, clean_hl, h_hash, tag, alpha))
            ins += 1
            print(f"📥 {clean_hl[:75]}...")
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print(f"\n✅ Modelo Citi Re-Rating V60.4.2 Inyectado: {ins} eventos procesados.")

if __name__ == "__main__":
    run_citi_rerating_model()
