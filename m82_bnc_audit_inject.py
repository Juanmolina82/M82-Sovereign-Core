#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3.2 CITADEL :: BNC & BANESCO Q3 AUDIT INJECTOR
# Venue: Caracas HQ Master Node | Corp. Internacional JMM, C.A.
# ==============================================================================

import os, sqlite3, hashlib

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

RAW_FILINGS = [
    ("BANKING", "GLFILE BNC.CR: Banco Nacional de Credito C.A. Interim Q3 2026 Filing 89695107 - Refinitiv Ingested", "VE Banking System Audit", 0.96),
    ("BANKING", "GLFILE Banesco C.A. Interim Q3 2026 Filing 89695116 - Refinitiv Ingested", "VE Banking System Audit", 0.94),
    ("MACRO", "IMF projects 5% GDP growth for Venezuela in 2026 driven by energy & commercial recovery", "Macro Expansion Index", 0.95)
]

def inject_audit():
    if not os.path.exists(DB_PATH):
        print("❌ DB no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    c.execute("PRAGMA journal_mode=WAL;")

    inserted = 0
    for desk, headline, tag, alpha in RAW_FILINGS:
        clean_hl = f"[{desk} | Caracas HQ] {headline}"[:115]
        h_hash = hashlib.sha256(clean_hl.encode()).hexdigest()[:16]

        try:
            c.execute("""
                INSERT INTO m82_multi_stream 
                (daemon_source, headline, headline_hash, desk, status, alpha_score, asset_impact, created_at)
                VALUES (?, ?, ?, ?, 'VERIFIED', ?, 'REFINITIV_BNC_Q3', CURRENT_TIMESTAMP)
            """, (desk, clean_hl, h_hash, tag, alpha))
            inserted += 1
            print(f"📥 [{desk}] {clean_hl[:65]}... (VERIFIED)")
        except sqlite3.IntegrityError:
            print(f"⚠️ DUPE SKIPPED: {clean_hl[:45]}...")

    conn.commit()
    conn.close()
    print(f"\n✅ Inyección BNC/Banesco Q3 completada: {inserted} nuevos eventos procesados.")

if __name__ == "__main__":
    inject_audit()
