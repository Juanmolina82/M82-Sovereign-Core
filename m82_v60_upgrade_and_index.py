#!/usr/bin/env python3
import os
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
DB_PATH = BASE_DIR / "m82_database.db"

def classify_desk(name: str, rel_path: str) -> tuple[str, int, int]:
    s = f"{rel_path}/{name}".lower()
    if any(k in s for k in ["supervisor", "orch.py", "master_dossier", "api_server", "fusion_engine", "core_orchestrator", "gateway"]):
        return ("CORE_ORCHESTRATION", 1, 30)
    if any(k in s for k in ["venezuela", "faja", "orinoco", "citgo", "machado", "delcy", "latam"]):
        return ("VENEZUELA_LATAM_DESK", 1, 60)
    if any(k in s for k in ["oil", "brent", "nymex", "energy", "lng", "gas", "uranium", "commodit", "hormuz", "iea"]):
        return ("GLOBAL_ENERGY_COMMODITIES_DESK", 1, 60)
    if any(k in s for k in ["geopolit", "war", "osint", "sanction", "ofac", "southcom", "tariffs", "gprk", "election"]):
        return ("GEOPOLITICS_TAIL_RISK_DESK", 1, 60)
    if any(k in s for k in ["refinitiv", "lseg", "bloomberg", "sec_13g", "ric_map", "market_close"]):
        return ("LSEG_REFINITIV_TERMINAL_DESK", 1, 60)
    if any(k in s for k in ["pe_", "vc_", "private", "megafund", "secondary", "deals", "exits", "vanguard", "blackrock"]):
        return ("PE_VENTURE_CAPITAL_DESK", 2, 120)
    if any(k in s for k in ["musk", "spacex", "tesla", "xai", "grok", "ai_", "semiconductor", "magnificent", "tpu", "agi"]):
        return ("AI_TECH_INFRA_DESK", 2, 120)
    if any(k in s for k in ["treasury", "fed", "rates", "cpi", "nfp", "labor", "credit", "bond", "sovereign", "yield", "stress"]):
        return ("MACRO_RATES_CREDIT_DESK", 1, 90)
    if any(k in s for k in ["crypto", "bitcoin", "stablecoin", "cbdc", "swift", "dedollar"]):
        return ("CRYPTO_MONETARY_DESK", 2, 180)
    return ("OBSERVABILITY_SHIELD_DESK", 2, 120)

def get_running_pids() -> dict[str, int]:
    running = {}
    try:
        out = subprocess.check_output(["ps", "-eo", "pid,args"], text=True)
        for line in out.splitlines()[1:]:
            parts = line.strip().split(None, 1)
            if len(parts) == 2 and parts[0].isdigit():
                running[parts[1]] = int(parts[0])
    except Exception:
        pass
    return running

def main():
    con = sqlite3.connect(str(DB_PATH), timeout=60.0)
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA busy_timeout=60000;")

    # 1. Deduplicar inserciones identicas recientes en macro_dossier
    con.execute("""
    DELETE FROM macro_dossier
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM macro_dossier
        GROUP BY source, category, headline
    );
    """)

    # 2. Migracion DDL v60 en macro_dossier
    existing_md = {r[1] for r in con.execute("PRAGMA table_info(macro_dossier)")}
    for col, col_def in [
        ("validated", "INTEGER DEFAULT 1"),
        ("alpha_score", "REAL DEFAULT 0.0"),
        ("tail_risk_index", "REAL DEFAULT 0.0"),
        ("desk_cluster", "TEXT DEFAULT 'CORE_MACRO'"),
    ]:
        if col not in existing_md:
            con.execute(f"ALTER TABLE macro_dossier ADD COLUMN {col} {col_def};")

    con.execute("""
    UPDATE macro_dossier
    SET
        validated = 1,
        alpha_score = ROUND(MAX(0.0, (sentiment + 1.0) * 1.15 - (risk_score * 0.12)), 3),
        tail_risk_index = ROUND(risk_score * (1.0 + CASE WHEN sentiment < 0 THEN ABS(sentiment) ELSE 0.0 END), 3),
        desk_cluster = CASE
            WHEN category LIKE '%VENEZUELA%' OR category LIKE '%LATAM%' THEN 'VENEZUELA_LATAM_DESK'
            WHEN category LIKE '%ENERGY%' OR category LIKE '%POWER%' THEN 'GLOBAL_ENERGY_DESK'
            WHEN category LIKE '%AI_%' OR category LIKE '%SEMICONDUCTOR%' OR category LIKE '%AEROSPACE%' THEN 'TECH_INFRA_AI_DESK'
            WHEN category LIKE '%EQUIT%' OR category LIKE '%MARKET%' OR category LIKE '%CAPITAL%' OR category LIKE '%LABOR%' THEN 'EQUITIES_MACRO_DESK'
            ELSE 'QUANT_TELEMETRY_CORE'
        END;
    """)

    # 3. Vistas institucionales v60
    con.executescript("""
    DROP VIEW IF EXISTS v_macro_dossier_matrix;
    CREATE VIEW v_macro_dossier_matrix AS
    SELECT
        desk_cluster,
        COUNT(*) AS total_dossiers,
        ROUND(AVG(risk_score), 3) AS avg_risk,
        ROUND(AVG(alpha_score), 3) AS avg_alpha,
        ROUND(AVG(tail_risk_index), 3) AS avg_tail_risk,
        ROUND(AVG(sentiment), 3) AS avg_sentiment,
        MAX(created_at) AS last_ingest_utc
    FROM macro_dossier
    WHERE validated = 1
    GROUP BY desk_cluster
    ORDER BY total_dossiers DESC;

    DROP VIEW IF EXISTS v_bunker_tail_risk_alerts;
    CREATE VIEW v_bunker_tail_risk_alerts AS
    SELECT
        rowid AS id,
        created_at,
        desk_cluster,
        category,
        risk_score,
        tail_risk_index,
        alpha_score,
        sentiment,
        m82_tag,
        headline
    FROM macro_dossier
    WHERE tail_risk_index >= 1.80 OR sentiment <= -0.25
    ORDER BY tail_risk_index DESC, created_at DESC;

    DROP VIEW IF EXISTS v_venezuela_energy_desk;
    CREATE VIEW v_venezuela_energy_desk AS
    SELECT
        rowid AS id,
        created_at,
        category,
        risk_score,
        alpha_score,
        sentiment,
        headline
    FROM macro_dossier
    WHERE desk_cluster IN ('VENEZUELA_LATAM_DESK', 'GLOBAL_ENERGY_DESK')
    ORDER BY created_at DESC;
    """)

    # 4. Asegurar columnas compatibles en m82_daemons_registry e indexar enjambre
    reg_cols = {r[1] for r in con.execute("PRAGMA table_info(m82_daemons_registry)")}
    if not reg_cols:
        con.executescript("""
        CREATE TABLE m82_daemons_registry (
            daemon_name TEXT PRIMARY KEY,
            script_path TEXT UNIQUE NOT NULL,
            desk_category TEXT NOT NULL,
            priority_tier INTEGER DEFAULT 2,
            poll_interval_sec INTEGER DEFAULT 60,
            status TEXT DEFAULT 'ACTIVE',
            last_pid INTEGER DEFAULT 0,
            is_running INTEGER DEFAULT 0,
            indexed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        reg_cols = {r[1] for r in con.execute("PRAGMA table_info(m82_daemons_registry)")}

    running_map = get_running_pids()
    discovered = []
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "node_modules", "mobile_build", "backups", "venv", ".venv"}]
        for fname in sorted(files):
            if not fname.endswith(".py") or fname in {"__init__.py", "m82_daemon_indexer.py", "m82_v60_upgrade_and_index.py"}:
                continue
            full_path = Path(root) / fname
            rel_path = str(full_path.relative_to(BASE_DIR))
            if not (fname.startswith("m82_") or fname.endswith(("_daemon.py", "_sentinel.py", "_bridge.py", "_engine.py", "_parser.py", "_ingest.py")) or fname in {"orch.py", "refinitiv_bridge.py", "ingest.py", "pwa_server.py", "wsgi_api.py"}):
                continue
            desk, tier, interval = classify_desk(fname, rel_path)
            pid = next((p for cmd, p in running_map.items() if fname in cmd), 0)
            discovered.append((fname, str(full_path), desk, tier, interval, pid, 1 if pid > 0 else 0))

    name_col = "daemon_name" if "daemon_name" in reg_cols else ("name" if "name" in reg_cols else list(reg_cols)[0])
    path_col = "script_path" if "script_path" in reg_cols else ("path" if "path" in reg_cols else None)
    desk_col = "desk_category" if "desk_category" in reg_cols else ("category" if "category" in reg_cols else None)
    stat_col = "status" if "status" in reg_cols else None

    for fname, fpath, desk, tier, interval, pid, is_run in discovered:
        cols = [name_col]
        vals = [fname]
        if path_col:
            cols.append(path_col); vals.append(fpath)
        if desk_col:
            cols.append(desk_col); vals.append(desk)
        if stat_col:
            cols.append(stat_col); vals.append("ACTIVE")
        if "last_pid" in reg_cols:
            cols.append("last_pid"); vals.append(pid)
        if "is_running" in reg_cols:
            cols.append("is_running"); vals.append(is_run)
        placeholders = ",".join("?" for _ in cols)
        con.execute(f"INSERT OR REPLACE INTO m82_daemons_registry ({','.join(cols)}) VALUES ({placeholders});", vals)

    con.commit()
    con.execute("PRAGMA wal_checkpoint(PASSIVE);")

    total_md = con.execute("SELECT COUNT(*) FROM macro_dossier").fetchone()[0]
    total_reg = con.execute("SELECT COUNT(*) FROM m82_daemons_registry").fetchone()[0]
    print(f"=== DDL v60 APLICADO OK | macro_dossier={total_md} filas limpias | m82_daemons_registry={total_reg} daemons ===")
    for r in con.execute("SELECT * FROM v_macro_dossier_matrix"):
        print(f"DESK: {r[0]:24s} | n={r[1]:3d} | risk={r[2]:.2f} | alpha={r[3]:.2f} | tail={r[4]:.2f} | sent={r[5]:+.2f}")
    if desk_col:
        print("\n=== DISTRIBUCION DE DAEMONS INDEXADOS ===")
        for r in con.execute(f"SELECT {desk_col}, COUNT(*) FROM m82_daemons_registry GROUP BY {desk_col} ORDER BY 2 DESC"):
            print(f"SWARM: {r[0]:32s} | indexados={r[1]:3d}")
    con.close()

if __name__ == "__main__":
    main()
