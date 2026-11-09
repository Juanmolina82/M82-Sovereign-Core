#!/usr/bin/env python3
# ==============================================================================
# M82 V60.4.1 CITADEL :: REFINITIV ESG PDF & WORKSPACE INJECTOR (D-51 / D-53)
# Venue: Caracas HQ Master Node | Corp. Internacional JMM C.A. / Molina Holdings
# ==============================================================================

import os, sqlite3, hashlib

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

ESG_PDF_TELEMETRY = [
    ("EQUITIES", "Citigroup (C.N) ESG Score 85.19 #1 Industry Rank — Env 94.66 #2 — Gov 92.06 #2 — Refinitiv EsgView PDF", "ESG_BENCHMARK_PDF", 0.99),
    ("EQUITIES", "Citi Controversies Drag: Score 1.02 D- pushes Combined Score to 43.11 — Re-Rating Catalyst Confirmed", "ESG_BENCHMARK_PDF", 0.98),
    ("TREASURY", "LPL Financial (LPLA.OQ) ESG Score 63.58 (Top 5) — Social Pillar 71.24 — LPL Compliance Desk", "LPL_COMPLIANCE", 0.96),
    ("EQUITIES", "Goldman Sachs (GS.N) Gov Score 94.34 #1 vs Morgan Stanley (MS.N) Env 78.55 — IB Peers Benchmark", "PEERS_BENCHMARK", 0.95)
]

def inject_pdf_esg():
    if not os.path.exists(DB_PATH):
        print("❌ DB no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA busy_timeout=60000;")

    ins = 0
    for desk, hl, tag, alpha in ESG_PDF_TELEMETRY:
        clean_hl = f"[{desk}] {hl}"[:120]
        h_hash = hashlib.sha256(clean_hl.encode()).hexdigest()[:16]

        try:
            c.execute("""
                INSERT INTO m82_multi_stream 
                (daemon_source, headline, headline_hash, desk, status, alpha_score, asset_impact, created_at)
                VALUES (?, ?, ?, ?, 'VERIFIED', ?, 'REFINITIV_ESG_PDF_INGEST', CURRENT_TIMESTAMP)
            """, (desk, clean_hl, h_hash, tag, alpha))
            ins += 1
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print(f"✅ Inyección Refinitiv ESG PDF: {ins} registros inyectados en m82_database.db")

if __name__ == "__main__":
    inject_pdf_esg()
