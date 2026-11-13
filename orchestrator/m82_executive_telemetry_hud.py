#!/usr/bin/env python3
import os, json, sqlite3
from datetime import datetime, timezone

M82_ROOT = os.path.expanduser("~/M82")
ORCH_DB = os.path.join(M82_ROOT, "m82_orchestrator_wal.db")

def render_hud():
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    conn = sqlite3.connect(f"file:{ORCH_DB}?mode=ro", uri=True, timeout=10.0)
    conn.execute("PRAGMA query_only = ON;")

    mission = conn.execute("SELECT tier_state, updated_at FROM m82_agent_missions WHERE mission_id='MISSION-CORE-001';").fetchone()
    swarm = conn.execute("SELECT audit_id, total_daemons, category_breakdown, core_db_status, audited_at FROM m82_swarm_audit_log ORDER BY audited_at DESC LIMIT 1;").fetchone()
    quant = conn.execute("SELECT quant_audit_id, exposure_x, dry_powder_pct, daily_var_pct, warsh_spread_bps, matched_tables, compliance_status FROM m82_quant_audit_ledger ORDER BY audited_at DESC LIMIT 1;").fetchone()
    routes = conn.execute("SELECT COUNT(*), SUM(kv_cache_hit), ROUND(AVG(est_ttft_ms), 2) FROM m82_llmd_routing_ledger;").fetchone()
    alerts = conn.execute("SELECT COUNT(*) FROM m82_governance_alerts;").fetchone()[0]
    tools = conn.execute("SELECT COUNT(*) FROM m82_mcp_registry;").fetchone()[0]
    conn.close()

    tier_state = mission[0] if mission else "UNKNOWN"
    total_reg = swarm[1] if swarm else 0
    cats = json.loads(swarm[2]) if swarm else {}
    live_ram = sum(cats.values())
    standby = max(0, total_reg - live_ram)
    core_status = swarm[3] if swarm else "N/A"

    exp_x, dry_pct, var_pct, warsh_bps, q_tables, comp_status = (quant[1], quant[2], quant[3], quant[4], quant[5], quant[6]) if quant else (0.22, 78.0, 1.68, 102.0, 0, "N/A")
    r_total, r_hits, r_ttft = (routes[0] or 0, routes[1] or 0, routes[2] or 0.0) if routes else (0, 0, 0.0)
    hit_rate = round((r_hits / r_total) * 100.0, 1) if r_total > 0 else 0.0

    line = "=" * 78
    print(f"\n{line}")
    print(f"  M82 SOVEREIGN CORE :: EXECUTIVE TELEMETRY HUD  |  {now_str}")
    print(f"  TOPOLOGIA DUAL: [NODO CHARALLAVE L4/L5 EDGE] <---> [CARACAS HQ CENTRAL]")
    print(f"{line}")
    print(f"  ESTADO MAESTRO : {tier_state} | MCP Tools Activas: {tools} | Alertas: {alerts}")
    print(f"  GOBERNANZA     : BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK [{comp_status}]")
    print(f"{'-' * 78}")
    print(f"  [1] RIESGO & CAPITAL (m82_database.db :: {core_status} | {q_tables}/76 tablas)")
    print(f"      - Exposicion Activa : {exp_x:.2f}x (Techo: 0.30x)   | Dry Powder : {dry_pct:.1f}%")
    print(f"      - VaR Diario        : {var_pct:.2f}% (Limite: 1.68%) | Warsh Spread: {warsh_bps:.1f} bps")
    print(f"{'-' * 78}")
    print(f"  [2] ENJAMBRE & TELEMETRIA (Watchdog TPU-Sync 300s)")
    print(f"      - Flota Registrada  : {total_reg} modulos | Vivos RAM: {live_ram} | Standby Bunker: {standby}")
    print(f"      - Desglose RAM      : {json.dumps(cats)}")
    print(f"{'-' * 78}")
    print(f"  [3] INFERENCIA DESAGREGADA LLMD 1.0 (Prefix-Cache-Aware Router)")
    print(f"      - Rutas Auditadas   : {r_total} | KV-Cache Hit Rate: {hit_rate}% | TTFT Promedio: {r_ttft} ms")
    print(f"{line}\n")

if __name__ == "__main__":
    render_hud()
