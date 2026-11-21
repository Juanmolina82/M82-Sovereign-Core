#!/usr/bin/env python3
import json
import os
import sqlite3
from datetime import datetime, timezone

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
OUT_JSON = os.path.join(BASE_DIR, "daily_dossier_latest.json")

conn = sqlite3.connect(DB_PATH, timeout=60.0, isolation_level=None)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")

now = datetime.now(timezone.utc).isoformat()
rows = conn.execute(
    "SELECT id, daemon_source, headline, status, timestamp FROM m82_multi_stream ORDER BY id DESC LIMIT 20"
).fetchall()

report = {
    "generated_at_utc": now,
    "topology": {"master": "CARACAS_HQ_CENTRAL", "execution": "CHARALLAVE_L4_L5_EDGE"},
    "governance": {
        "mode": "BUNKER_MODE_CUSTODIA_PASIVA_030X_LOCK",
        "active_exposure": "0.22x",
        "daily_var": "1.68%",
        "warsh_spread_bps": 102.0,
        "policy": "LOCKOUT: NO TRADE",
    },
    "recent_signals": [
        {"id": r[0], "source": r[1], "headline": r[2], "status": r[3], "timestamp": r[4]}
        for r in rows
    ],
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

conn.execute(
    "INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp) VALUES ('DAILY_DOSSIER_CRON', ?, 'PENDING', ?)",
    (f"DAILY DOSSIER CONSOLIDATED [{now[:19]}Z]: {len(rows)} Signals | Charallave Edge -> Caracas HQ | BUNKER 0.30x LOCK", now),
)
conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()
print(f"✅ Dossier diario generado en {OUT_JSON} ({len(rows)} señales).")
