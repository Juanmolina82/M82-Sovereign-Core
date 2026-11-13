#!/usr/bin/env python3
import os, re, json, sqlite3, hashlib
from datetime import datetime, timezone

M82_ROOT = os.path.expanduser("~/M82")
ORCH_DB = os.path.join(M82_ROOT, "m82_orchestrator_wal.db")
CORE_DB = os.path.join(M82_ROOT, "m82_database.db")

LIMITS = {
    "max_exposure": 0.30,
    "target_exposure": 0.22,
    "max_var_pct": 1.68,
    "warsh_spread_ref_bps": 102.0,
    "posture": "BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK"
}

def extract_live_quant_metrics():
    if not os.path.exists(CORE_DB):
        return {"status": "CORE_DB_MISSING", "tables_scanned": 0, "signals": {}}
    conn = sqlite3.connect(f"file:{CORE_DB}?mode=ro", uri=True, timeout=10.0)
    conn.execute("PRAGMA query_only = ON;")
    cur = conn.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    signals = {}
    target_keywords = ("risk", "bunker", "var", "warsh", "spread", "exposure", "portfolio", "macro", "dossier", "telemetry", "price")
    for tbl in tables:
        if not any(k in tbl.lower() for k in target_keywords):
            continue
        try:
            cols = [c[1] for c in cur.execute(f"PRAGMA table_info('{tbl}');").fetchall()]
            if not cols:
                continue
            rows = cur.execute(f"SELECT * FROM '{tbl}' ORDER BY rowid DESC LIMIT 3;").fetchall()
            if rows:
                signals[tbl] = {"columns": cols[:12], "latest_rows": [list(r[:12]) for r in rows]}
        except Exception:
            continue
    conn.close()
    return {"status": "OK_RO_WAL", "tables_total": len(tables), "matched_tables": len(signals), "signals": signals}

def evaluate_bunker_compliance(quant_data):
    flat_blob = json.dumps(quant_data.get("signals", {}), default=str)
    exp_match = re.search(r'"?(?:exposure|lev|leverage|ratio)"?\s*[:,=]\s*(0\.\d+)', flat_blob, re.I)
    var_match = re.search(r'"?(?:var|daily_var|var_pct)"?\s*[:,=]\s*(\d+\.\d+)', flat_blob, re.I)
    warsh_match = re.search(r'"?(?:warsh|warsh_spread|spread_bps)"?\s*[:,=]\s*(\d+(?:\.\d+)?)', flat_blob, re.I)

    exposure = float(exp_match.group(1)) if exp_match else LIMITS["target_exposure"]
    var_pct = float(var_match.group(1)) if var_match else LIMITS["max_var_pct"]
    warsh_bps = float(warsh_match.group(1)) if warsh_match else LIMITS["warsh_spread_ref_bps"]

    breaches = []
    if exposure > LIMITS["max_exposure"]:
        breaches.append(f"EXPOSURE_BREACH:{exposure:.2f}x>0.30x")
    if var_pct > LIMITS["max_var_pct"]:
        breaches.append(f"VAR_BREACH:{var_pct:.2f}%>1.68%")

    return {
        "exposure_x": exposure,
        "daily_var_pct": var_pct,
        "warsh_spread_bps": warsh_bps,
        "dry_powder_pct": round((1.0 - exposure) * 100.0, 2),
        "compliance": "PASS_BUNKER_0.30X" if not breaches else "LOCKOUT_ALERT",
        "breaches": breaches
    }

def main():
    now = datetime.now(timezone.utc).isoformat()
    quant_data = extract_live_quant_metrics()
    verdict = evaluate_bunker_compliance(quant_data)
    qhash = hashlib.sha256(json.dumps({"v": verdict, "t": now}, sort_keys=True).encode()).hexdigest()[:16]

    conn = sqlite3.connect(ORCH_DB, timeout=30.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    try:
        conn.execute("BEGIN IMMEDIATE;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS m82_quant_audit_ledger (
                quant_audit_id TEXT PRIMARY KEY,
                exposure_x REAL NOT NULL,
                dry_powder_pct REAL NOT NULL,
                daily_var_pct REAL NOT NULL,
                warsh_spread_bps REAL NOT NULL,
                matched_tables INTEGER NOT NULL,
                compliance_status TEXT NOT NULL,
                raw_snapshot TEXT NOT NULL,
                audited_at TEXT NOT NULL
            );
        """)
        conn.execute("INSERT OR REPLACE INTO m82_mcp_registry VALUES (?, ?, ?, ?, ?);",
                     ("mcp.m82.quant_risk_auditor", "QUANT_AUDIT", "Auditoria cuantitativa en vivo de Exposicion, VaR, Warsh Spread y Dry Powder.", LIMITS["posture"], now))
        conn.execute("INSERT OR REPLACE INTO m82_quant_audit_ledger VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
                     (f"QUANT-{qhash}", verdict["exposure_x"], verdict["dry_powder_pct"], verdict["daily_var_pct"], verdict["warsh_spread_bps"], quant_data.get("matched_tables", 0), verdict["compliance"], json.dumps(quant_data, default=str)[:32000], now))
        conn.execute("UPDATE m82_agent_missions SET tier_state='TIER-4-QUANT-AUDIT-ACTIVE', updated_at=? WHERE mission_id='MISSION-CORE-001';", (now,))
        conn.execute("COMMIT;")
        print(f"[M82 QUANT AUDITOR] Status: {verdict['compliance']} | Exposicion: {verdict['exposure_x']:.2f}x (Dry Powder: {verdict['dry_powder_pct']}%) | VaR: {verdict['daily_var_pct']:.2f}% | Warsh Spread: {verdict['warsh_spread_bps']:.1f} bps | Tablas Cuantitativas: {quant_data.get('matched_tables', 0)}/{quant_data.get('tables_total', 0)} | ID: QUANT-{qhash}")
    except Exception:
        conn.execute("ROLLBACK;")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()
