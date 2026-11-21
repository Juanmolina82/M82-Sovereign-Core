#!/usr/bin/env python3
import os, sqlite3
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

NEW_SIGNALS = [
    ("SAMSUNG_AI_BOOM", "Samsung flags $8.0B profit on AI boom, highest quarterly for tech sector", 0.89, "BTCUSD"),
    ("SAUDI_YEMEN_ATTACK", "Attacks on Saudi exports kill two people as fighting escalates in Yemen", 0.94, "BRENT"),
    ("US_MORTGAGE_RATES", "US 30-year mortgage rate hits highest level in nearly 15 years amid yield curve pressure", -0.62, "US10Y")
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for src, text, alpha, asset in NEW_SIGNALS:
    headline = f"[{src} | {now_str}] {text}"
    try:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
            VALUES (?, ?, 'PENDING', ?, ?)
        """, (src, headline, alpha, asset))
        print(f"🔥 [INYECTADO] {src} -> Alpha: {alpha}")
    except Exception as e:
        print(f"⚠️ Error: {e}")

conn.commit()
conn.close()
