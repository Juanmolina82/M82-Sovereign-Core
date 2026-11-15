#!/usr/bin/env python3
import os, time, json, sqlite3, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_orchestrator_wal.db")
SYMBOLS = {"CL=F": "WTI CRUDE", "BZ=F": "BRENT CRUDE", "RB=F": "RBOB GAS", "HO=F": "HEATING OIL", "^TNX": "US 10Y", "DX-Y.NYB": "DXY", "NVDA": "NVIDIA", "BTC-USD": "BTC-USD"}
RSS_FEEDS = ["https://feeds.finance.yahoo.com/rss/2.0/headline?s=CL=F,NVDA,SPY&region=US&lang=en-US", "https://www.cnbc.com/id/100003114/device/rss/rss.html"]

def fetch_quotes():
    out = []
    for sym, label in SYMBOLS.items():
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m&range=1d"
            req = urllib.request.Request(url, headers={"User-Agent": "M82-Sovereign-Engine/4.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                meta = json.loads(r.read().decode("utf-8"))["chart"]["result"][0]["meta"]
                px = float(meta.get("regularMarketPrice"))
                prev = float(meta.get("chartPreviousClose") or px)
                chg = ((px - prev) / prev * 100.0) if prev else 0.0
                out.append((sym, label, round(px, 2), round(chg, 2)))
        except Exception:
            pass
    return out

def fetch_headlines():
    items = []
    for feed in RSS_FEEDS:
        try:
            req = urllib.request.Request(feed, headers={"User-Agent": "M82-Sovereign-Engine/4.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                root = ET.fromstring(r.read())
                for item in root.findall(".//item")[:5]:
                    t = (item.findtext("title") or "").strip()
                    if t:
                        items.append(t)
        except Exception:
            pass
    return items

def sync_cycle():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    cur = conn.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    quotes, headlines = fetch_quotes(), fetch_headlines()
    target_tbl = next((t for t in tables if any(k in t.lower() for k in ("news", "wire", "event", "feed", "dispatch", "log"))), None)
    if target_tbl:
        cols = [c[1] for c in cur.execute(f"PRAGMA table_info({target_tbl})").fetchall()]
        if len(cols) >= 3:
            for q_sym, q_lbl, q_px, q_chg in quotes[:4]:
                cur.execute(f"INSERT INTO {target_tbl} ({cols[1]}, {cols[2]}) VALUES (?, ?)", (now_iso, f"[M82 QUANTUM TELEMETRY] {q_lbl} ({q_sym}): {q_px} ({q_chg:+.2f}%) | BUNKER 0.30x LOCK"))
            for hl in headlines[:5]:
                clean_hl = hl.replace("Reuters", "M82 Global").replace("LSEG", "M82 Wire")
                cur.execute(f"INSERT INTO {target_tbl} ({cols[1]}, {cols[2]}) VALUES (?, ?)", (now_iso, f"[M82 MACRO WIRE] {clean_hl}"))
    conn.commit()
    conn.close()
    print(f"[{now_iso}] WAL Sync OK: {len(quotes)} activos + {len(headlines)} titulares.")

if __name__ == "__main__":
    while True:
        try:
            sync_cycle()
        except Exception as e:
            print(f"[M82 FEED WARN] {e}")
        time.sleep(60)
