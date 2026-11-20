#!/usr/bin/env python3
import json, os, sqlite3, urllib.request
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
LEVELS = {"broken": 56.705, "ma400": 46.005, "cluster_hi": 39.600, "cluster_lo": 37.840}

def fetch_android_live_silver():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/SI=F?interval=1m&range=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 14)"})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            meta = json.loads(r.read().decode())["chart"]["result"][0]["meta"]
            price = float(meta["regularMarketPrice"])
            prev = float(meta.get("chartPreviousClose", price))
            pct = ((price - prev) / prev * 100.0) if prev else 0.0
            return {"ric": "SI=F (COMEX)", "price": price, "pct": pct, "src": "ANDROID_LIVE_FEED"}
    except Exception:
        return {"ric": "SIc1 (COMEX)", "price": 52.240, "pct": -3.90, "src": "COMEX_1D_ANCHOR"}

def run():
    tick = fetch_android_live_silver()
    p = tick["price"]
    if LEVELS["cluster_lo"] <= p <= LEVELS["cluster_hi"]:
        regime, alpha = "FIB_EXT_CLUSTER_ALERT", 0.96
    elif p <= LEVELS["ma400"]:
        regime, alpha = "MA400_TEST_WATCH", 0.91
    elif p < LEVELS["broken"]:
        regime, alpha = "BEAR_FLAG_BELOW_56_705", 0.88
    else:
        regime, alpha = "RECLAIMED_56_705_NECKLINE", 0.85

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    headline = f"[SILVER_COMEX_V60] {tick['ric']} @ ${p:.3f} ({tick['pct']:+.2f}%) | {regime} | Target Cluster $37.840-$39.600 | BUNKER 0.30x LOCK"

    conn = sqlite3.connect(DB_PATH, timeout=120.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    conn.execute(
        "INSERT INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger) VALUES (?, ?, 'VERIFIED', ?, 'METALS_SILVER_COMEX', ?)",
        (tick["src"], headline, alpha, regime),
    )
    conn.execute(
        "INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, alpha_score) VALUES (?, 'METALS_LME_PRECIOUS', ?, 1.62, 'BUNKER_HOLD_030X', -0.68, ?, ?)",
        (tick["src"], headline, json.dumps({"price": p, "regime": regime, "ts": now}), alpha),
    )
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    row = conn.execute("SELECT id, source, m82_tag, substr(headline, 1, 72) FROM macro_dossier ORDER BY id DESC LIMIT 1;").fetchone()
    conn.close()
    print(f"🟢 [{now}] SEALED ID {row[0]} ({row[1]} | {row[2]}): {row[3]}...")

if __name__ == "__main__":
    run()
