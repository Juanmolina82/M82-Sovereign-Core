#!/usr/bin/env python3
import os, re, glob, json, sqlite3, hashlib, subprocess
from datetime import datetime, timezone

M82_ROOT = os.path.expanduser("~/M82")
ORCH_DB = os.path.join(M82_ROOT, "m82_orchestrator_wal.db")
CORE_DB = os.path.join(M82_ROOT, "m82_database.db")

POLICY = {
    "posture": "BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK",
    "max_exposure_cap": 0.30,
    "target_exposure": 0.22,
    "daily_var_limit_pct": 1.68,
    "warsh_spread_ref_bps": 102.0,
    "zero_plaintext_secrets": True,
    "egress_mode": "ALLOWLIST_STRICT",
    "node": "Charallave L4/L5 Edge"
}

TOOLS = [
    ("mcp.m82.swarm_discovery", "READ_ONLY", "Censo dual: procesos vivos en RAM + catalogo completo de daemons en disco/SQLite."),
    ("mcp.m82.bunker_risk_guard", "AUDIT_ENFORCE", "Verificacion continua de exposicion (<=0.30x), VaR diario y Warsh Spread."),
    ("mcp.m82.wal_checkpoint_sync", "STATE_PERSIST", "Serializacion de estado multi-dia patron TPU Sync en m82_orchestrator_wal.db."),
    ("mcp.m82.refinitiv_telemetry_probe", "READ_ONLY", "Sonda de frescura sobre m82_refinitiv_realtime_bridge y feeds de mercado.")
]

def discover_live_processes():
    live = []
    out = subprocess.check_output(["ps", "-eo", "pid,etime,args"], text=True, stderr=subprocess.DEVNULL)
    for line in out.splitlines()[1:]:
        parts = line.strip().split(None, 2)
        if len(parts) < 3:
            continue
        pid_s, etime, cmd = parts
        if any(k in cmd for k in ("/M82/", "m82_", "orch.py", "desks/", "lseg_websocket", "price_feeder")):
            if "m82_mcp_governance_gateway.py" in cmd or "ps -eo" in cmd:
                continue
            m = re.search(r"([a-zA-Z0-9_./-]+\.(?:py|sh))", cmd)
            name = os.path.basename(m.group(1)) if m else cmd[:60]
            cat = "COMMODITY_DESK" if "desks/" in cmd else (
                "TELEMETRY_BRIDGE" if any(t in cmd for t in ("refinitiv", "lseg", "feeder", "ingest")) else (
                    "SUPERVISOR_CORE" if any(s in cmd for s in ("orch.py", "supervisor", "watchdog", "dossier")) else "AGENT_WORKER"
                )
            )
            live.append({"pid": int(pid_s), "name": name, "category": cat, "uptime": etime, "cmd": cmd[:180]})
    return live

def discover_registered_modules():
    patterns = [
        os.path.join(M82_ROOT, "m82_*.py"),
        os.path.join(M82_ROOT, "orch.py"),
        os.path.join(M82_ROOT, "force_dispatch.py"),
        os.path.join(M82_ROOT, "desks", "*.py"),
        os.path.join(M82_ROOT, "scripts", "*.py"),
        os.path.join(M82_ROOT, "orchestrator", "*.py"),
        os.path.join(M82_ROOT, "v2", "**", "*.py"),
        os.path.join(M82_ROOT, "v3", "**", "*.py"),
    ]
    files = set()
    for pat in patterns:
        for f in glob.glob(pat, recursive=True):
            if os.path.isfile(f) and not f.endswith(".bak"):
                files.add(os.path.relpath(f, M82_ROOT))
    return sorted(files)

def probe_core():
    if not os.path.exists(CORE_DB):
        return {"status": "CORE_DB_NOT_FOUND", "table_count": 0}
    try:
        c = sqlite3.connect(f"file:{CORE_DB}?mode=ro", uri=True, timeout=5.0)
        c.execute("PRAGMA query_only = ON;")
        n = len(c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
        c.close()
        return {"status": "HEALTHY_RO_WAL", "table_count": n}
    except Exception as e:
        return {"status": f"BUSY: {e}", "table_count": 0}

def main():
    live = discover_live_processes()
    registered = discover_registered_modules()
    live_names = {d["name"] for d in live}
    standby = [r for r in registered if os.path.basename(r) not in live_names]
    core = probe_core()
    now = datetime.now(timezone.utc).isoformat()

    cats = {}
    for d in live:
        cats[d["category"]] = cats.get(d["category"], 0) + 1

    summary = {
        "timestamp_utc": now,
        "live_processes_count": len(live),
        "registered_modules_count": len(registered),
        "standby_modules_count": len(standby),
        "live_breakdown": cats,
        "core_db": core,
        "policy": POLICY
    }
    h = hashlib.sha256(json.dumps(summary, sort_keys=True).encode()).hexdigest()

    conn = sqlite3.connect(ORCH_DB, timeout=30.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA busy_timeout=30000;")
    try:
        conn.execute("BEGIN IMMEDIATE;")
        conn.execute("CREATE TABLE IF NOT EXISTS m82_mcp_registry (tool_id TEXT PRIMARY KEY, scope TEXT, description TEXT, policy_lock TEXT, registered_at TEXT);")
        conn.execute("CREATE TABLE IF NOT EXISTS m82_swarm_audit_log (audit_id TEXT PRIMARY KEY, total_daemons INTEGER, category_breakdown TEXT, daemon_inventory TEXT, core_db_status TEXT, governance_posture TEXT, audited_at TEXT);")
        for tid, sc, desc in TOOLS:
            conn.execute("INSERT OR REPLACE INTO m82_mcp_registry VALUES (?, ?, ?, ?, ?);", (tid, sc, desc, POLICY["posture"], now))
        inventory_payload = json.dumps({"live": live, "registered_total": len(registered), "standby": standby})
        conn.execute("INSERT OR REPLACE INTO m82_swarm_audit_log VALUES (?, ?, ?, ?, ?, ?, ?);",
                     (f"AUDIT-{h[:16]}", len(registered), json.dumps(cats), inventory_payload, core["status"], POLICY["posture"], now))
        conn.execute("UPDATE m82_agent_missions SET tier_state='TIER-2-MCP-GATEWAY-ACTIVE', checkpoint_payload=?, updated_at=? WHERE mission_id='MISSION-CORE-001';",
                     (json.dumps(summary), now))
        conn.execute("COMMIT;")
        print(f"[M82 MCP GATEWAY] Registrados en Flota: {len(registered)} | Vivos en RAM: {len(live)} {json.dumps(cats)} | Standby (Bunker): {len(standby)} | CoreDB: {core['status']} ({core['table_count']} tablas) | Hash: {h[:16]}")
    except Exception:
        conn.execute("ROLLBACK;")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()
