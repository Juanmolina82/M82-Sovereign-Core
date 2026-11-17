#!/usr/bin/env python3
import os, time, sqlite3, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
HUB_URL = "http://127.0.0.1:8286/api/workspace/ingest"

def sync_cycle():
    last_id = 0
    while True:
        try:
            conn = sqlite3.connect(DB_PATH, timeout=60.0)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=60000;")
            cur = conn.cursor()
            rows = cur.execute("SELECT id, daemon_source, headline FROM m82_multi_stream WHERE id > ? ORDER BY id ASC LIMIT 25", (last_id,)).fetchall()
            conn.close()
            for rid, src, hdl in rows:
                last_id = max(last_id, rid)
                s = f"{src} {hdl}".upper()
                if any(k in s for k in ["NVDA", "MSFT", "JPM", "XLK", "COIN", "RTX", "RIO"]):
                    tab = "COMPANIES"
                elif any(k in s for k in ["AI", "WARSH", "OPEC", "HORMUZ", "FED"]):
                    tab = "TRENDING_TOPICS"
                elif any(k in s for k in ["ALERT", "CRITICAL", "BUNKER", "DOSSIER"]):
                    tab = "TOP_NEWS"
                else:
                    tab = "LATEST_NEWS"
                requests.post(HUB_URL, json={"tab": tab, "headline": hdl, "sector": src or "LSEG_WIRE"}, timeout=5)
        except Exception as e:
            print(f"[!] Sync: {e}", flush=True)
        time.sleep(15)

if __name__ == "__main__":
    sync_cycle()
