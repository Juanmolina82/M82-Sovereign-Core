#!/usr/bin/env python3
import os, sys, time, sqlite3, subprocess, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"

def trigger_mcm_live_ingest():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    headline = "[MCM LIVE] María Corina Machado ofrece primeras declaraciones tras regreso a Venezuela — YouTube Live IL80ZRWkm2g (Transmisión Transición & Plan País)"
    tag = "v61.0.1-MCM-LIVE-2026-10-29"

    cur.execute("""
        INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json)
        VALUES ('M82_POLITICS_VZ', 'POLITICAL_TRANSITION', ?, 2.50, ?, 0.85, '{"stream_id":"IL80ZRWkm2g","user":"jmmp@molina82.com","schedule":"11:45AM-12:00PM"}')
    """, (headline, tag))

    cur.execute("""
        INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
        VALUES ('M82_POLITICS_DESK', '[LIVE] MCM Retorno Venezuela — Cobertura Rueda de Prensa En Vivo YouTube', 'BREAKOUT_ACTIVE', 0.98, 'VENEZUELA_POLITICS', 'MCM_PRESS_CONFERENCE')
    """, ())

    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    # Disparar renderizado de tarjeta HUD sanitizada D-34
    subprocess.run(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "B"], check=False)
    print("🟢 [MCM LIVE WATCHER] Evento registrado y tarjeta HUD D-34 enviada a Telegram.")

if __name__ == "__main__":
    trigger_mcm_live_ingest()
