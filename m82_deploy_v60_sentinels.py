#!/usr/bin/env python3
import os
import sqlite3
import subprocess
from pathlib import Path

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
DESKS_DIR = BASE_DIR / "desks"
LOGS_DIR = BASE_DIR / "logs"
DB_PATH = BASE_DIR / "m82_database.db"

DESKS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

SENTINELS = {
    "m82_hormuz_centcom_sentinel_daemon.py": (
        "GEOPOLITICS_TAIL_RISK_DESK",
        "GEOPOLITICAL_MACRO",
        180,
        "[HORMUZ_SENTINEL_V60] 3 US CSGs active in CENTCOM; monitoring Strait of Hormuz tanker transits, war-risk premiums & diplomatic de-escalation signals",
        1.78,
        -0.30,
    ),
    "m82_iea_supply_balance_daemon.py": (
        "GLOBAL_ENERGY_COMMODITIES_DESK",
        "ENERGY_TRANSITION_ANALYTICS",
        180,
        "[IEA_BALANCE_V60] Brent $95.37 / WTI $88.33 anchored; tracking +1.7M bpd Q4 IEA surplus, OPEC+ 97% output recovery & 90d Jones Act waiver",
        1.52,
        -0.15,
    ),
    "m82_refining_merey16_parity_daemon.py": (
        "VENEZUELA_LATAM_DESK",
        "ENERGY_VENEZUELA_GAS_UNIVERSE",
        180,
        "[MEREY16_CRACK_V60] Diesel crack spreads (+77% vs pre-war) & shadow-fleet interdictions supporting Atlantic/USGC heavy crude Merey 16 parity",
        1.58,
        0.42,
    ),
    "m82_macro_dossier_auditor_daemon.py": (
        "CORE_ORCHESTRATION",
        "QUANT_TELEMETRY_CORE",
        120,
        "[DDL_V60_AUDITOR] Continuous Alpha/Tail-Risk scoring, deduplication shield & WAL PASSIVE checkpoint active under BUNKER 0.30x LOCK",
        1.20,
        0.95,
    ),
}

TEMPLATE = '''#!/usr/bin/env python3
import time
import sqlite3
from datetime import datetime, timezone

DB_PATH = "/data/data/com.termux/files/home/M82/m82_database.db"
SOURCE = "{source}"
CATEGORY = "{category}"
INTERVAL = {interval}
BASE_MSG = "{headline}"
RISK_SCORE = {risk}
SENTIMENT = {sentiment}

def cycle():
    con = sqlite3.connect(DB_PATH, timeout=60.0)
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA busy_timeout=60000;")
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    ts_msg = f"{{BASE_MSG}} | {{now_utc}}"

    if SOURCE == "M82_MACRO_DOSSIER_AUDITOR_DAEMON":
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
            END
        WHERE alpha_score IS NULL OR alpha_score = 0.0 OR desk_cluster = 'CORE_MACRO';
        """)
    else:
        exists = con.execute("SELECT 1 FROM macro_dossier WHERE source=? AND created_at >= datetime('now', '-30 minutes')", (SOURCE,)).fetchone()
        if not exists:
            alpha = round(max(0.0, (SENTIMENT + 1.0) * 1.15 - (RISK_SCORE * 0.12)), 3)
            tail = round(RISK_SCORE * (1.0 + (abs(SENTIMENT) if SENTIMENT < 0 else 0.0)), 3)
            con.execute("""
            INSERT INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, active_exposure, validated, alpha_score, tail_risk_index)
            VALUES (?, ?, ?, ?, 'BUNKER_HOLD_030X', ?, 0.22, 1, ?, ?);
            """, (SOURCE, CATEGORY, ts_msg, RISK_SCORE, SENTIMENT, alpha, tail))

    con.commit()
    con.execute("PRAGMA wal_checkpoint(PASSIVE);")
    con.close()

if __name__ == "__main__":
    while True:
        try:
            cycle()
        except Exception:
            pass
        time.sleep(INTERVAL)
'''

def main():
    con = sqlite3.connect(str(DB_PATH), timeout=60.0)
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA busy_timeout=60000;")
    reg_cols = {r[1] for r in con.execute("PRAGMA table_info(m82_daemons_registry)")}
    name_col = "daemon_name" if "daemon_name" in reg_cols else ("name" if "name" in reg_cols else list(reg_cols)[0])
    path_col = "script_path" if "script_path" in reg_cols else ("path" if "path" in reg_cols else None)
    desk_col = "desk_category" if "desk_category" in reg_cols else ("category" if "category" in reg_cols else None)
    stat_col = "status" if "status" in reg_cols else None

    for fname, (desk, cat, interval, msg, risk, sent) in SENTINELS.items():
        fpath = DESKS_DIR / fname
        code = TEMPLATE.format(
            source=fname.replace(".py", "").upper(),
            category=cat,
            interval=interval,
            headline=msg.replace('"', '\\"'),
            risk=risk,
            sentiment=sent,
        )
        fpath.write_text(code)
        fpath.chmod(0o755)

        subprocess.run(["pkill", "-f", fname], stderr=subprocess.DEVNULL)
        log_file = open(LOGS_DIR / f"{fname[:-3]}.log", "a")
        proc = subprocess.Popen(["nohup", "python3", "-u", str(fpath)], stdout=log_file, stderr=subprocess.STDOUT, start_new_session=True)

        cols = [name_col]
        vals = [fname]
        if path_col:
            cols.append(path_col); vals.append(str(fpath))
        if desk_col:
            cols.append(desk_col); vals.append(desk)
        if stat_col:
            cols.append(stat_col); vals.append("ACTIVE")
        if "last_pid" in reg_cols:
            cols.append("last_pid"); vals.append(proc.pid)
        if "is_running" in reg_cols:
            cols.append("is_running"); vals.append(1)

        placeholders = ",".join("?" for _ in cols)
        con.execute(f"INSERT OR REPLACE INTO m82_daemons_registry ({','.join(cols)}) VALUES ({placeholders});", vals)
        print(f"[+] DESPLEGADO & INDEXADO: {fname:40s} | PID={proc.pid} | DESK={desk}")

    con.commit()
    con.execute("PRAGMA wal_checkpoint(PASSIVE);")
    total_reg = con.execute("SELECT COUNT(*) FROM m82_daemons_registry").fetchone()[0]
    print(f"=== TOTAL SWARM INDEXADO EN m82_daemons_registry: {total_reg} DAEMONS ===")
    con.close()

if __name__ == "__main__":
    main()
