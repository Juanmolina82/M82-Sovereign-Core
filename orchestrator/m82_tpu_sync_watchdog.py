#!/usr/bin/env python3
import os, sys, time, json, sqlite3, subprocess
from datetime import datetime, timezone

M82_ROOT = os.path.expanduser("~/M82")
ORCH_DB = os.path.join(M82_ROOT, "m82_orchestrator_wal.db")
GATEWAY_SCRIPT = os.path.join(M82_ROOT, "orchestrator", "m82_mcp_governance_gateway.py")
INTERVAL_SEC = 300

def init_alert_table():
    conn = sqlite3.connect(ORCH_DB, timeout=30.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("CREATE TABLE IF NOT EXISTS m82_governance_alerts (alert_id TEXT PRIMARY KEY, severity TEXT NOT NULL, category TEXT NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL);")
    conn.close()

def evaluate_health():
    now = datetime.now(timezone.utc).isoformat()
    subprocess.run([sys.executable, GATEWAY_SCRIPT], check=True)
    conn = sqlite3.connect(ORCH_DB, timeout=30.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    row = conn.execute("SELECT audit_id, total_daemons, category_breakdown, core_db_status FROM m82_swarm_audit_log ORDER BY audited_at DESC LIMIT 1;").fetchone()
    if row:
        audit_id, total_reg, breakdown_json, core_status = row
        cats = json.loads(breakdown_json)
        alerts = []
        if cats.get("TELEMETRY_BRIDGE", 0) < 1:
            alerts.append(("CRITICAL", "TELEMETRY_HEARTBEAT", "TELEMETRY_BRIDGE sin procesos activos en RAM."))
        if cats.get("SUPERVISOR_CORE", 0) < 1:
            alerts.append(("CRITICAL", "SUPERVISOR_HEARTBEAT", "SUPERVISOR_CORE sin procesos activos en RAM."))
        if "HEALTHY" not in core_status:
            alerts.append(("WARNING", "CORE_DB_CONTENTION", f"Estado CoreDB anomalo: {core_status}"))
        for idx, (sev, cat, msg) in enumerate(alerts):
            conn.execute("INSERT OR REPLACE INTO m82_governance_alerts VALUES (?, ?, ?, ?, ?);", (f"{audit_id}-A{idx}", sev, cat, msg, now))
        print(f"[M82 TPU-SYNC WATCHDOG] {now} | Audit: {audit_id} | Flota: {total_reg} | RAM: {cats} | Alertas: {len(alerts)}", flush=True)
    conn.close()

def main():
    init_alert_table()
    if "--once" in sys.argv:
        evaluate_health()
        return
    while True:
        try:
            evaluate_health()
        except Exception as e:
            print(f"[M82 TPU-SYNC WATCHDOG ERROR] {datetime.now(timezone.utc).isoformat()} | {e}", flush=True)
        time.sleep(INTERVAL_SEC)

if __name__ == "__main__":
    main()
