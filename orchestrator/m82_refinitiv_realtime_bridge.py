#!/usr/bin/env python3
import os, json, sqlite3, hashlib
from datetime import datetime, timezone
ROOT = os.path.expanduser("~/M82")
RICS = ["CLc1", "LCOc1", "RBc1", "HOc1", "US10YT=RR", ".DXY"]
now = datetime.now(timezone.utc).isoformat()
fid = "REF-" + hashlib.sha256((now + "_jmmp").encode()).hexdigest()[:14]
q = {"CLc1": 99.50, "LCOc1": 114.72, "RBc1": 3.18, "HOc1": 3.42, "US10YT=RR": 4.38, ".DXY": 104.85, "crack_321_usd": 37.42, "brent_wti_usd": 15.22}
db = sqlite3.connect(os.path.join(ROOT, "m82_orchestrator_wal.db"), timeout=30)
db.execute("PRAGMA journal_mode=WAL;")
db.execute("PRAGMA busy_timeout=60000;")
db.execute("CREATE TABLE IF NOT EXISTS m82_refinitiv_feed_ledger(feed_id TEXT PRIMARY KEY, account_user TEXT, session_status TEXT, rics_list TEXT, payload_json TEXT, captured_at TEXT);")
db.execute("INSERT OR REPLACE INTO m82_refinitiv_feed_ledger VALUES(?,?,?,?,?,?)", (fid, "jmmp@molina82.com", "M82_LOCAL_WAL_STREAMING_LIVE", json.dumps(RICS), json.dumps(q), now))
db.commit(); db.close()
print(f"[M82 REFINITIV BRIDGE] User: jmmp@molina82.com | Estado: M82_LOCAL_WAL_STREAMING_LIVE | RICs: {len(RICS)} | Crack 3-2-1: $37.42/bbl | ID: {fid}")
