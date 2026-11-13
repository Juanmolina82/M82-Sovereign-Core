#!/usr/bin/env python3
import os, json, sqlite3
db = sqlite3.connect(os.path.expanduser("~/M82/m82_orchestrator_wal.db"), timeout=30)
db.execute("PRAGMA journal_mode=WAL;"); db.execute("PRAGMA busy_timeout=60000;")
row = db.execute("SELECT feed_id, session_status, payload_json, captured_at FROM m82_refinitiv_feed_ledger ORDER BY captured_at DESC LIMIT 1").fetchone()
db.close()
if row:
    q = json.loads(row[2])
    print(f"=== M82 GERENTE HUD | BUNKER 0.30x LOCK ===\nEstado: {row[1]} | ID: {row[0]}\nWTI (CLc1): ${q['CLc1']} | Brent (LCOc1): ${q['LCOc1']} | Spread B-W: ${q['brent_wti_usd']}\nRBOB: ${q['RBc1']} | HO: ${q['HOc1']} | Crack 3-2-1: ${q['crack_321_usd']}/bbl\nUST 10Y: {q['US10YT=RR']}% | DXY: {q['.DXY']}\nTimestamp UTC: {row[3]}")
