#!/usr/bin/env python3
import os, sqlite3
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

SIGNALS_008 = [
    ("CHEVRON_GULF_CUT", "Shell and Chevron cut Gulf of Mexico output as Tropical Storm Isaias approaches", 0.84, "WTI"),
    ("CRUDE_LOGISTICS_BOTTLE", "Oil new problem is not supply it is logistics as transit risks escalate", 0.78, "BRENT"),
    ("TIN_LME_AI_WAVE", "Tin rides the AI investment wave to a new price dimension as demand surges", 0.67, "BTCUSD"),
    ("US_POWER_SUMMER_TEST", "Renewables help US power system survive summer stress test amid datacenter demand", 0.42, "MACRO")
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for src, text, alpha, asset in SIGNALS_008:
    headline = f"[{src} | {now_str}] {text}"
    try:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
            VALUES (?, ?, 'PENDING', ?, ?)
        """, (src, headline, alpha, asset))
        print(f"🔥 [INYECTADO M82] {src} -> Alpha: {alpha} | Asset: {asset}")
    except Exception as e:
        print(f"⚠️ Error: {e}")

conn.commit()
conn.close()
