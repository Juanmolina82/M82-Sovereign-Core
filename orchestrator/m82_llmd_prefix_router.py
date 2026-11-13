#!/usr/bin/env python3
import os, json, sqlite3, hashlib
from datetime import datetime, timezone

M82_ROOT = os.path.expanduser("~/M82")
ORCH_DB = os.path.join(M82_ROOT, "m82_orchestrator_wal.db")

POOLS_LLMD = {
    "PREFILL_HEAVY": {"pool_id": "llmd-tpu8t-prefill-01", "role": "PREFILL", "max_ctx": 131072, "policy": "BUNKER_0.30x"},
    "DECODE_LOW_LATENCY": {"pool_id": "llmd-tpu8i-decode-01", "role": "DECODE", "max_ctx": 32768, "policy": "BUNKER_0.30x"},
    "QUANT_AUDIT_LOCAL": {"pool_id": "charallave-edge-l4-l5", "role": "HYBRID_EDGE", "max_ctx": 16384, "policy": "BUNKER_0.30x"}
}

PREFIX_SIGNATURES = {
    "M82_MACRO_DOSSIER": "M82-FULL-STACK-TPUV8-LLMD1-AGENT-RUNTIME-2026",
    "M82_COMMODITY_CRACKS": "M82-CRACK-SPREADS-OFFTAKE-REQUEST-POOL",
    "M82_BUNKER_TAILRISK": "M82-BUNKER-0.30X-WARSH-102BPS-VAR-1.68"
}

def init_schema(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS m82_llmd_routing_ledger (route_id TEXT PRIMARY KEY, workload_type TEXT, prefix_hash TEXT, target_pool TEXT, kv_cache_hit INTEGER, est_ttft_ms REAL, routed_at TEXT);")
    conn.execute("INSERT OR REPLACE INTO m82_mcp_registry VALUES (?, ?, ?, ?, ?);",
                 ("mcp.m82.llmd_prefix_router", "INFERENCE_ROUTE", "Enrutamiento desagregado LLMD 1.0 con cache de prefijos KV bajo BUNKER 0.30x.", "BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK", datetime.now(timezone.utc).isoformat()))

def route_workload(conn, wtype, pkey, qtext, ctx_tokens):
    now = datetime.now(timezone.utc).isoformat()
    phash = hashlib.sha256(PREFIX_SIGNATURES.get(pkey, pkey).encode()).hexdigest()[:24]
    prev = conn.execute("SELECT COUNT(*) FROM m82_llmd_routing_ledger WHERE prefix_hash=?;", (phash,)).fetchone()[0]
    kv_hit = 1 if prev > 0 else 0
    if ctx_tokens > 32768 and not kv_hit:
        pool, ttft = POOLS_LLMD["PREFILL_HEAVY"], 145.0
    elif wtype == "EDGE_AUDIT":
        pool, ttft = POOLS_LLMD["QUANT_AUDIT_LOCAL"], (18.5 if kv_hit else 34.0)
    else:
        pool, ttft = POOLS_LLMD["DECODE_LOW_LATENCY"], (22.0 if kv_hit else 58.0)
    rid = f"ROUTE-{hashlib.sha256(f'{now}_{phash}_{qtext}'.encode()).hexdigest()[:14]}"
    conn.execute("INSERT OR REPLACE INTO m82_llmd_routing_ledger VALUES (?, ?, ?, ?, ?, ?, ?);", (rid, wtype, phash, pool["pool_id"], kv_hit, ttft, now))
    return {"route_id": rid, "pool": pool["pool_id"], "kv_hit": bool(kv_hit), "ttft_ms": ttft}

def main():
    conn = sqlite3.connect(ORCH_DB, timeout=30.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    try:
        conn.execute("BEGIN IMMEDIATE;")
        init_schema(conn)
        r1 = route_workload(conn, "MACRO_INGEST", "M82_MACRO_DOSSIER", "Indexar dossier TPU v8", 64000)
        r2 = route_workload(conn, "EDGE_AUDIT", "M82_BUNKER_TAILRISK", "Auditar Warsh Spread 102bps", 4096)
        r3 = route_workload(conn, "EDGE_AUDIT", "M82_BUNKER_TAILRISK", "Verificar VaR 1.68% y techo 0.30x", 4096)
        now = datetime.now(timezone.utc).isoformat()
        payload = json.dumps({"tier": "TIER-3-LLMD-ROUTER-ACTIVE", "pools": list(POOLS_LLMD.keys()), "sample_routes": [r1, r2, r3], "updated_at": now})
        conn.execute("UPDATE m82_agent_missions SET tier_state='TIER-3-LLMD-ROUTER-ACTIVE', checkpoint_payload=?, updated_at=? WHERE mission_id='MISSION-CORE-001';", (payload, now))
        conn.execute("COMMIT;")
        print(f"[M82 LLMD 1.0 ROUTER] Ruta 1: {r1['pool']} (TTFT {r1['ttft_ms']}ms, KV-Hit: {r1['kv_hit']}) | Ruta 2 (Cold): {r2['pool']} ({r2['ttft_ms']}ms, KV-Hit: {r2['kv_hit']}) | Ruta 3 (Warm Hit): {r3['pool']} ({r3['ttft_ms']}ms, KV-Hit: {r3['kv_hit']})")
    except Exception:
        conn.execute("ROLLBACK;")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()
