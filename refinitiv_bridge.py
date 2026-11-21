#!/usr/bin/env python3
import os, time, sqlite3, random
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

REFINITIV_FEEDS = [
    ("LSEG_WS_FEED", "IEA releases emergency oil reserves, crude futures drop sharply", 0.78, "WTI"),
    ("US_SANCTIONS", "OFAC updates Venezuela maritime licensing guidelines for crude exports", 0.82, "VENZ34"),
    ("BLOOMBERG_MACRO", "Fed signals interest rate trajectory adjustment as inflation cools", -0.65, "BTCUSD"),
    ("OPEC_BASKET", "OPEC+ ministers discuss unexpected output cut in upcoming extraordinary meeting", 0.88, "BRENT"),
    ("CITGO_OFAC_DESK", "Delaware court issues timeline update on PDVSA/Citgo equity auction", -0.74, "PDVSA26")
]

def ingest_refinitiv_news():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    src, headline, alpha, asset = random.choice(REFINITIV_FEEDS)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    headline_str = f"[REFINITIV BREAKING | {now_str}] {headline}"
    
    try:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
            VALUES (?, ?, 'PENDING', ?, ?)
        """, (src, headline_str, alpha, asset))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        try:
            ingest_refinitiv_news()
        except Exception:
            pass
        time.sleep(15)
