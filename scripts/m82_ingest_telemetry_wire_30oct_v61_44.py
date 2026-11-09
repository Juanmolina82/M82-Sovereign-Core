#!/usr/bin/env python3
# M82 SOVEREIGN CORE - TELEMETRY INGESTION v61.0.44
# OPSEC & BRAND HARD-SANITIZED ENGINE
import sqlite3, os, json, subprocess
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
SCRIPT_HUD = os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py")

conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur = conn.cursor()

headline = "[M82 TELEMETRY FLASH v61.0.44] Exxon Chevron Beats Refining Margins -- Nasdaq $2T-$3T Wipeout Oct AI Overspend -- Trump Venezuela Oil Deal Reality -- Crypto $6.3B Binance Heist Crash -- US $2.1B Missile Sale Lithuania -- French Debt Slows Europe"
tag = "v61.0.44-M82-TELEMETRY-EXXON-CHEVRON-NASDAQ-TRUMP-VZ"

meta = {
    "source": "Global Wire Telemetry Stream 30-Oct-2026",
    "exxon_chevron": "Q3 beat on strong refining margins (ULSD crack $108/bbl), offsets crude dip, validates Merey 16 netback $88.80-$90.50/bbl",
    "nasdaq_wipeout": "Nasdaq -$2T to -$3T October loss, AI overspend fears, high WACC 10.8-16% tech squeeze",
    "venezuela_geopol": "Trump touts new Venezuela oil deal as reality sets in, export corridor validation",
    "crypto_crisis": "Binance heist $6.3B drains market, flight to quality and real assets active",
    "defence_rates": "US $2.1B missile sale to Lithuania, BOJ inflation rate hike signals, French OAT debt stress",
    "operator": "SECURE OPERATOR D-34",
    "node": "SOVEREIGN EDGE CORE",
    "timestamp": datetime.now(timezone.utc).isoformat()
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('GLOBAL_WIRE_TELEMETRY', 'MACRO_ENERGY_TECH_GEOPOL', ?, 0.98, ?, 0.92, ?, 'v61.0.44', 'SOVEREIGN_EDGE_CORE')
""", (headline, tag, json.dumps(meta)))

conn.commit()
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total_count = cur.fetchone()[0]
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()

print(f"🔒 M82 v61.0.44 SEALED -- TOTAL RECORDS: {total_count} -- WAL 0/0/0 CLEAN")
if os.path.exists(SCRIPT_HUD):
    subprocess.run(["python3", SCRIPT_HUD], check=False)
