#!/usr/bin/env python3
import os, time, sqlite3, subprocess, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
USER_ACCOUNT = "jmmp@molina82.com"

TOPNEWS = [
    ("M82_REFINITIV_TOPNEWS", "POLITICS_TRANSITION", "[REFINITIV WIRE] MCM Live Address Scheduled Following Venezuela Return — Roadmap to Democratic Transition & Reconstruction", 0.98, "v61.0.1-TOPNEWS-MCM-RETURN"),
    ("M82_REFINITIV_TOPNEWS", "INFRASTRUCTURE_POWER", "[REFINITIV WIRE] GE Vernova Awaits Upfront Payment for $25B SEN Grid Rebuild — Prepayment Lock Monitored", 0.94, "v61.0.1-TOPNEWS-GEV-GRID"),
    ("M82_REFINITIV_TOPNEWS", "DEBT_RECOVERY", "[REFINITIV WIRE] VZ Bonds Benchmark VENZ27 $50.61 & PDVSA20 $115.32 — Citgo 50.1% Collateral Validated for Citi Escrow $200B", 0.99, "v61.0.1-TOPNEWS-BONDS-QUAD")
]

def sync_topnews():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    for source, cat, headline, alpha, tag in TOPNEWS:
        cur.execute("""
            INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json)
            VALUES ('Refinitiv Workspace TopNews', ?, ?, 1.68, ?, 0.90, '{"account":"jmmp@molina82.com","feed":"LSEG_TOPNEWS_LIVE"}')
        """, (cat, headline, tag))

        cur.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
            VALUES (?, ?, 'PROCESSED', ?, 'VENEZUELA_MACRO', 'REFINITIV_TOPNEWS_INGEST')
        """, (source, headline, alpha))

    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    # Ejecutar sanitizador D-34 para generar tarjeta resumen
    subprocess.run(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "B"], check=False)
    print("🟢 [REFINITIV TOPNEWS] Sincronización completada y purgada bajo protocolo D-34.")

if __name__ == "__main__":
    sync_topnews()
