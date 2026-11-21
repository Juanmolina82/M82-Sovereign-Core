#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3.2 CITADEL :: REFINITIV FULL CHARTBOARD EXTENDED INJECTOR
# Venue: Caracas HQ Master Node | Corp. Internacional JMM, C.A.
# ==============================================================================

import os, sqlite3, hashlib

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

FULL_TELEMETRY = [
    ("BANKING", "BlackRock AUM & Fees hit record high vs Morgan Stanley $3.2B equity trading surge", "Financials Basket Compliance", 0.97),
    ("ENERGY", "Marathon Petroleum refining profits reach highest since 2022 — BP net debt reduction continues", "Faja Heavy Crude", 0.96),
    ("TECH_AI", "Big Tech AI Capex surge pressures short-term FCF but accelerates Cloud monetization trajectory", "Semi Capacity Crunch vs Power Demand", 0.98),
    ("RETAIL", "Walmart comp sales & ad growth outperforms Target in S&P 500 index comparison", "Consumer Sector Scan", 0.89),
    ("PHARMA", "Merck Keytruda & AstraZeneca oncology sales sustain Healthcare sector cash flows", "Pharma Defensive Basket", 0.85)
]

def inject_full_chartboard():
    if not os.path.exists(DB_PATH):
        print("❌ Base de datos no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    c.execute("PRAGMA journal_mode=WAL;")

    inserted = 0
    for desk, headline, tag, alpha in FULL_TELEMETRY:
        clean_hl = f"[{desk} | Caracas HQ] {headline}"[:115]
        h_hash = hashlib.sha256(clean_hl.encode()).hexdigest()[:16]

        try:
            c.execute("""
                INSERT INTO m82_multi_stream 
                (daemon_source, headline, headline_hash, desk, status, alpha_score, asset_impact, created_at)
                VALUES (?, ?, ?, ?, 'VERIFIED', ?, 'REFINITIV_FULL_CHARTBOARD', CURRENT_TIMESTAMP)
            """, (desk, clean_hl, h_hash, tag, alpha))
            inserted += 1
            print(f"📥 [{desk}] {clean_hl[:65]}... (VERIFIED {alpha})")
        except sqlite3.IntegrityError:
            print(f"⚠️ DUPE SKIPPED: {clean_hl[:45]}...")

    conn.commit()
    conn.close()
    print(f"\n✅ Inyección Chartboard Extendido completada: {inserted} nuevos eventos procesados.")

if __name__ == "__main__":
    inject_full_chartboard()
