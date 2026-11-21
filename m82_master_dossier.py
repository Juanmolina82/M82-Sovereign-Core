#!/usr/bin/env python3
import os, time, sqlite3, random
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

MACRO_EVENT_POOL = [
    ("VENZ34_DEBT", "Venezuela sovereign debt restructured trading range updated", 0.75, "VENZ34"),
    ("LATAM_POLITICS", "LatAm energy corridor bilateral trade agreement signed", 0.45, "WTI"),
    ("SWIFT_FLOWS", "Cross-border settlement volume spikes in energy clearing desk", 0.60, "WTI"),
    ("CITGO_OFAC_DESK", "OFAC extends protection license for Citgo assets", 0.80, "PDVSA26"),
    ("PDVSA26_SWAPS", "PDVSA bond yield curve shifts following crude export report", -0.55, "PDVSA26"),
    ("WTI_FUTURES", "Crude oil futures react to unexpected inventory drawdown", 0.68, "WTI")
]

def daemon_worker():
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            source, headline_text, base_alpha, asset = random.choice(MACRO_EVENT_POOL)
            alpha_score = round(base_alpha + random.uniform(-0.05, 0.05), 2)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            headline = f"[{source} | {now_str}] {headline_text}"
            
            c.execute("""
                INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
                VALUES (?, ?, 'PENDING', ?, ?)
            """, (source, headline, alpha_score, asset))
            
            conn.commit()
            conn.close()
        except Exception:
            pass
        
        time.sleep(random.randint(30, 60))

if __name__ == "__main__":
    daemon_worker()
