#!/usr/bin/env python3
import os, sqlite3
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

SIGNALS_939 = [
    ("HOUTHI_SAUDI_MISSILE", "How Houthi missiles strike on Saudi airports along a 500-kilometer regional corridor", 0.91, "BRENT"),
    ("CENOVUS_BP_DEAL", "Canada Cenovus Energy funds $8.8B acquisition of British Petroleum crude assets", 0.79, "WTI"),
    ("FED_MINUTES_RATE", "Fed Minutes signal possible rate increase this year with no urgency for October hike", -0.58, "US10Y"),
    ("GLOBAL_BOND_YIELDS", "Bond yields surging around the world across major economies while China diverges", 0.64, "XAUUSD")
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for src, text, alpha, asset in SIGNALS_939:
    headline = f"[{src} | {now_str}] {text}"
    try:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
            VALUES (?, ?, 'PENDING', ?, ?)
        """, (src, headline, alpha, asset))
        print(f"🔥 [INYECTADO M82] {src} -> Alpha: {alpha}")
    except Exception as e:
        print(f"⚠️ Error: {e}")

conn.commit()
conn.close()
