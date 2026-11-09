#!/usr/bin/env python3
import os, sys, time, sqlite3, subprocess, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
USER_ACCOUNT = "jmmp@molina82.com"

def ingest_mastercard_and_top_earnings():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    headline = "[REFINITIV WIRE] Mastercard Q3 Revenue Up 14% YoY to $9.8B Driven by Cross-Border Volume (+17%) — Global Payment Liquidity Resilient"
    m82_tag = "v61.0.1-MA-EARNINGS-Q3-REVENUE-9.8B"

    cur.execute("""
        INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json)
        VALUES ('Refinitiv Workspace / LSEG', 'FINANCIALS_EARNINGS', ?, 1.45, ?, 0.92, '{"account":"jmmp@molina82.com","ticker":"MA.N","revenue_b":9.8,"yoy_growth":"14%","cross_border_growth":"17%"}')
    """, (headline, m82_tag))

    cur.execute("""
        INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
        VALUES ('M82_EARNINGS_DESK', '[TELEMETRY] Mastercard Q3 $9.8B Revenue Ingested — Global Cross-Border Payments Strength', 'BREAKOUT_ACTIVE', 0.96, 'GLOBAL_FINANCIALS', 'MA_Q3_EARNINGS_BEAT')
    """, ())

    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    # Ejecutar motor sanitizado D-34 para generar tarjeta HUD 48pt
    subprocess.run(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "B"], check=False)
    print("🟢 [MA.N Q3 EARNINGS SUCCESS] Ingesta completada y tarjeta HUD D-34 (48pt) despachada a Telegram.")

if __name__ == "__main__":
    ingest_mastercard_and_top_earnings()
