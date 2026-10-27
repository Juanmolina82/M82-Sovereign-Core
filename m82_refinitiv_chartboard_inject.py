#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3.1 CITADEL :: REFINITIV CHARTBOARD INJECTOR
# Venue: Caracas HQ Master Node | Corp. Internacional JMM, C.A. / Molina Holdings LLC
# ==============================================================================

import os, sqlite3, hashlib
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

CHARTBOARD_TELEMETRY = [
    ("BANKING", "JPMorgan & Wells Fargo equity trading surge offsets BAC $1.2B AML penalty", "Financials Basket Compliance", 0.94),
    ("RETAIL", "Walmart advertising & retail strength outperforms Target in S&P 500 index comparison", "Consumer Sector Scan", 0.88),
    ("ENERGY", "Refining margins remain near multi-year highs as BP cuts net debt to $13.5B-$14.5B range", "Faja Heavy Crude", 0.96),
    ("TECH_AI", "Big Tech Cloud growth accelerates driven by generative AI enterprise workload adoption", "Semi Capacity Crunch vs Power Demand", 0.98)
]

def inject_chartboard():
    if not os.path.exists(DB_PATH):
        print("❌ DB no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    c.execute("PRAGMA journal_mode=WAL;")

    inserted = 0

    for desk, headline, tag, alpha in CHARTBOARD_TELEMETRY:
        clean_hl = f"[{desk} | Caracas HQ] {headline}"[:115]
        h_hash = hashlib.sha256(clean_hl.encode()).hexdigest()[:16]

        try:
            c.execute("""
                INSERT INTO m82_multi_stream 
                (daemon_source, headline, headline_hash, desk, status, alpha_score, asset_impact, created_at)
                VALUES (?, ?, ?, ?, 'VERIFIED', ?, 'REFINITIV_CHARTBOARD', CURRENT_TIMESTAMP)
            """, (desk, clean_hl, h_hash, tag, alpha))
            inserted += 1
            print(f"📥 [{desk}] {clean_hl[:65]}... (VERIFIED)")
        except sqlite3.IntegrityError:
            print(f"⚠️ DUPE SKIPPED: {clean_hl[:45]}...")

    conn.commit()
    conn.close()
    print(f"\n✅ Inyección Refinitiv Chartboard completada: {inserted} nuevos eventos procesados.")

if __name__ == "__main__":
    inject_chartboard()
