#!/usr/bin/env python3
import os, sys, sqlite3, datetime, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"

def dispatch_dual():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    cur = conn.cursor()
    
    ts = datetime.datetime.now().strftime("%H:%M:%S ET")
    headline = (
        f"[{ts}] DUAL-TRACK DASHBOARD :: TRACK A (NABEP REAL): 200K bpd | Costo $30 | 35% Pentágono Warrants "
        f"vs TRACK B (MCM RESERVE): $17.14BN/año | Merey $93.92 | WACC 7.5% | Citi Escrow"
    )
    
    cur.execute("""
        INSERT OR IGNORE INTO m82_multi_stream 
        (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
        VALUES ('M82_DUAL_TRACK_DASH', ?, 'PENDING', 0.99, 'SOVEREIGN_DUAL_TRACK', 'DUAL_VIEW_SYNC')
    """, (headline,))
    
    conn.commit()
    conn.close()
    print("🟢 [SUCCESS] Evento Dual-Track encolado para generación de Tarjeta HUD HD (54pt).")

if __name__ == "__main__":
    dispatch_dual()
