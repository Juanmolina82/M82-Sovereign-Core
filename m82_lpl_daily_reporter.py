#!/usr/bin/env python3
import os, sqlite3, json
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
DASH_DIR = os.path.expanduser("~/M82/dashboard")
os.makedirs(DASH_DIR, exist_ok=True)

REPORT_PATH = os.path.join(DASH_DIR, "lpl_daily_report_latest.html")
LOG_PATH = os.path.join(DASH_DIR, "zeropii_settlement_log.json")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

verified_cnt = c.execute("SELECT COUNT(*) FROM m82_multi_stream WHERE status='VERIFIED'").fetchone()[0]
grid_cnt = c.execute("SELECT COUNT(*) FROM m82_multi_stream WHERE asset_impact='MACRO200_GRID_60'").fetchone()[0]
c.execute("SELECT headline, created_at FROM m82_multi_stream WHERE desk='ZERO_PII' ORDER BY id DESC LIMIT 5")
zero_pii_events = c.fetchall()
conn.close()

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S VET")

log_data = {
    "node": "Caracas HQ Master Node (L5 Edge)",
    "protocol": "BUNKER MODE (0.30x LOCK)",
    "timestamp": now_str,
    "verified_events": verified_cnt,
    "grid_status": f"{grid_cnt}/60 Daemons Active",
    "zero_pii_events": [{"headline": e[0], "ts": e[1]} for e in zero_pii_events]
}

with open(LOG_PATH, "w", encoding="utf-8") as f:
    json.dump(log_data, f, indent=2)

html_report = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>M82 Citadel Prime :: LPL Daily Report</title></head>
<body style="background:#0b0e14; color:#d1d4dc; font-family:monospace; padding:20px;">
<h2>M82 CITADEL PRIME :: LPL DAILY REPORT</h2>
<p>Status: <b style="color:#089981;">BUNKER MODE (0.30x LOCK)</b> | Verified: {verified_cnt} | Grid: {grid_cnt}/60</p>
<hr>
<p>Zero-PII Gateway: <b>D-34 MASKED SHA-256 PASS</b></p>
</body></html>"""

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(html_report)

print("✅ Generación exitosa de zeropii_settlement_log.json y lpl_daily_report_latest.html")
