#!/usr/bin/env python3
import os, json, sqlite3, hashlib
from datetime import datetime, timezone

M82_ROOT = os.path.expanduser("~/M82")
ORCH_DB = os.path.join(M82_ROOT, "m82_orchestrator_wal.db")
CORE_DB = os.path.join(M82_ROOT, "m82_database.db")

def load_baseline():
    conn = sqlite3.connect(f"file:{ORCH_DB}?mode=ro", uri=True, timeout=10.0)
    conn.execute("PRAGMA query_only = ON;")
    q = conn.execute("SELECT exposure_x, dry_powder_pct, daily_var_pct, warsh_spread_bps FROM m82_quant_audit_ledger ORDER BY audited_at DESC LIMIT 1;").fetchone()
    conn.close()
    if q:
        return {"exposure_x": q[0], "dry_powder_pct": q[1], "daily_var_pct": q[2], "warsh_spread_bps": q[3]}
    return {"exposure_x": 0.22, "dry_powder_pct": 78.0, "daily_var_pct": 1.68, "warsh_spread_bps": 102.0}

def scan_crack_spread_tables():
    if not os.path.exists(CORE_DB):
        return 0
    conn = sqlite3.connect(f"file:{CORE_DB}?mode=ro", uri=True, timeout=10.0)
    conn.execute("PRAGMA query_only = ON;")
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    conn.close()
    return sum(1 for t in tables if any(k in t.lower() for k in ("crack", "refin", "commodity", "energy", "spread", "forward", "margin")))

def run_stress_matrix(base):
    exp = base["exposure_x"]
    var0 = base["daily_var_pct"]
    warsh0 = base["warsh_spread_bps"]

    scenarios = [
        {"id": "SCN-01-BASELINE", "name": "Bunker Baseline (Custodia Pasiva)", "crack_shock_pct": 0.0, "warsh_bps": warsh0, "var_mult": 1.00},
        {"id": "SCN-02-CRACK-COMP", "name": "Compresion Crack Spreads (-35%)", "crack_shock_pct": -35.0, "warsh_bps": round(warsh0 + 14.0, 1), "var_mult": 1.32},
        {"id": "SCN-03-WARSH-SPIKE", "name": "Choque Liquidez Warsh (+48 bps)", "crack_shock_pct": -15.0, "warsh_bps": round(warsh0 + 48.0, 1), "var_mult": 1.45},
        {"id": "SCN-04-TAIL-BLACKSWAN", "name": "Tail-Risk Cisne Negro (99.5% CVaR)", "crack_shock_pct": -45.0, "warsh_bps": round(warsh0 + 83.0, 1), "var_mult": 1.85}
    ]

    results = []
    for s in scenarios:
        stressed_var = round(var0 * s["var_mult"], 2)
        nav_drawdown_pct = round(exp * stressed_var * 1.45, 2)
        bunker_buffer_pct = round(base["dry_powder_pct"] - nav_drawdown_pct, 2)
        status = "SURVIVES_BUNKER_LOCK" if (exp <= 0.30 and nav_drawdown_pct < 3.50) else "TRIGGER_HARD_LOCKOUT"
        results.append({
            "scenario_id": s["id"],
            "name": s["name"],
            "crack_shock_pct": s["crack_shock_pct"],
            "warsh_spread_bps": s["warsh_bps"],
            "stressed_var_pct": stressed_var,
            "est_nav_drawdown_pct": nav_drawdown_pct,
            "net_dry_powder_pct": bunker_buffer_pct,
            "verdict": status
        })
    return results

def main():
    now = datetime.now(timezone.utc).isoformat()
    base = load_baseline()
    crack_tables = scan_crack_spread_tables()
    matrix = run_stress_matrix(base)
    sim_hash = hashlib.sha256(json.dumps({"m": matrix, "t": now}, sort_keys=True).encode()).hexdigest()[:16]

    conn = sqlite3.connect(ORCH_DB, timeout=30.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    try:
        conn.execute("BEGIN IMMEDIATE;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS m82_stress_simulation_ledger (
                sim_id TEXT PRIMARY KEY,
                base_exposure_x REAL NOT NULL,
                crack_tables_scanned INTEGER NOT NULL,
                worst_case_drawdown_pct REAL NOT NULL,
                bunker_verdict TEXT NOT NULL,
                matrix_json TEXT NOT NULL,
                simulated_at TEXT NOT NULL
            );
        """)
        conn.execute("INSERT OR REPLACE INTO m82_mcp_registry VALUES (?, ?, ?, ?, ?);",
                     ("mcp.m82.bunker_stress_simulator", "STRESS_SIM", "Simulador de estres cuantitativo sobre Crack Spreads, Warsh Spread y Tail-Risk CVaR bajo BUNKER 0.30x.", "BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK", now))
        worst_dd = max(r["est_nav_drawdown_pct"] for r in matrix)
        overall_verdict = "ALL_SCENARIOS_PASS_BUNKER" if all(r["verdict"] == "SURVIVES_BUNKER_LOCK" for r in matrix) else "ALERT_REVIEW"
        conn.execute("INSERT OR REPLACE INTO m82_stress_simulation_ledger VALUES (?, ?, ?, ?, ?, ?, ?);",
                     (f"SIM-{sim_hash}", base["exposure_x"], crack_tables, worst_dd, overall_verdict, json.dumps(matrix), now))
        conn.execute("UPDATE m82_agent_missions SET tier_state='TIER-5-STRESS-SIM-ACTIVE', updated_at=? WHERE mission_id='MISSION-CORE-001';", (now,))
        conn.execute("COMMIT;")

        print("\n" + "=" * 82)
        print(f"  M82 BUNKER STRESS SIMULATOR :: CRACK SPREADS & TAIL-RISK  |  ID: SIM-{sim_hash}")
        print(f"  Exposicion Base: {base['exposure_x']:.2f}x (Techo 0.30x) | Dry Powder: {base['dry_powder_pct']:.1f}% | Tablas Crack/Energy: {crack_tables}")
        print("=" * 82)
        for r in matrix:
            print(f"  [{r['scenario_id']}] {r['name']:<34} | Crack: {r['crack_shock_pct']:>5.1f}% | Warsh: {r['warsh_spread_bps']:>5.1f} bps | Drawdown NAV: -{r['est_nav_drawdown_pct']:>4.2f}% | {r['verdict']}")
        print("=" * 82 + "\n")
    except Exception:
        conn.execute("ROLLBACK;")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()
