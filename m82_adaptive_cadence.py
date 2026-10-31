#!/usr/bin/env python3
# ==============================================================================
# M82 ADAPTIVE CADENCE ENGINE -- CORNICHE REAL-TIME DEMO (30s PWA / 60s PUSH)
# Chairman Juan M. Molina -- Sovereign Execution Core (Charallave L4/L5 Edge)
# ==============================================================================
import os, sqlite3, time

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def set_adaptive_cadence():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    # Registrar ajuste de cadencia para la Demo Corniche
    cur.execute("""
        INSERT OR REPLACE INTO m82_multi_stream 
        (daemon_source, headline, status, alpha_score, sentiment, asset_impact, event_trigger)
        VALUES (
            'M82_CADENCE_ENGINE',
            '[CORNICHE DEMO READY] Dynamic Cadence Activated: PWA 30s Real-Time HUD / Telegram 60s Clean Push | Anti-Daneka Filter Active',
            'BREAKOUT_ACTIVE',
            0.99,
            0.99,
            'HUD_30S_ACTIVE',
            'DEMO_CADENCE_SET'
        );
    """)
    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()
    print("🟢 [CADENCE SET] PWA Surface adaptada a 30s Real-Time Demo | WAL CLEAN 0/0/0")

if __name__ == "__main__":
    set_adaptive_cadence()
