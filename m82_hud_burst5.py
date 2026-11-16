
def _m82_live_banner():
    try:
        import sqlite3 as _s
        _c = _s.connect("file:/data/data/com.termux/files/home/M82/m82_database.db?mode=ro", uri=True, timeout=15.0)
        _r = _c.execute("SELECT btc_price, btc_chg_pct, merey16_price, wti_price, wti_chg_pct, brent_price FROM m82_live_market_quotes WHERE id=1").fetchone()
        _c.close()
        if _r and _r[0]:
            return f"BTC: ${_r[0]:,.0f} ({_r[1]:+.2f}%) | MEREY 16: ${_r[2]:.2f} | WTI: ${_r[3]:.2f} | BRENT: ${_r[5]:.2f}"
    except Exception:
        pass
    return "BTC: LIVE | MEREY 16: LIVE | WTI: LIVE | BRENT: LIVE"

#!/usr/bin/env python3
import os
import re
import time
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
DB_PATH = BASE_DIR / "m82_database.db"
BURST_SIZE = 5

def init_burst_state():
    con = sqlite3.connect(str(DB_PATH), timeout=60.0)
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA busy_timeout=60000;")
    con.executescript("""
    CREATE TABLE IF NOT EXISTS m82_hud_dispatch_log (
        dossier_rowid INTEGER PRIMARY KEY,
        source TEXT,
        desk_cluster TEXT,
        dispatched_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    con.commit()
    con.execute("PRAGMA wal_checkpoint(PASSIVE);")
    con.close()

def get_live_banner():
    try:
        con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, timeout=15.0)
        r = con.execute("SELECT merey16_price, wti_price, wti_chg_pct, brent_price FROM m82_live_market_quotes WHERE id=1").fetchone()
        con.close()
        if r:
            return _m82_live_banner()
    except Exception:
        pass
    return _m82_live_banner()

def pull_burst_batch(limit=BURST_SIZE):
    con = sqlite3.connect(str(DB_PATH), timeout=60.0)
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA busy_timeout=60000;")

    rows = con.execute("""
    SELECT rowid, source, COALESCE(desk_cluster, 'GLOBAL_MACRO_FED'), headline,
           ROUND(COALESCE(alpha_score, 1.0), 2), ROUND(COALESCE(tail_risk_index, 1.5), 2)
    FROM macro_dossier
    WHERE rowid NOT IN (SELECT dossier_rowid FROM m82_hud_dispatch_log)
      AND lower(headline) NOT LIKE '%book review:%'
      AND lower(headline) NOT LIKE '%the fed explained%'
    GROUP BY source ORDER BY MAX(rowid) DESC
    LIMIT ?;
    """, (limit,)).fetchall()

    # Si ya se despacharon todos los nuevos, rotar los 5 de mayor Alpha/Tail-Risk recientes
    if len(rows) < limit:
        extra = con.execute("""
        SELECT rowid, source, COALESCE(desk_cluster, 'GLOBAL_MACRO_FED'), headline,
               ROUND(COALESCE(alpha_score, 1.0), 2), ROUND(COALESCE(tail_risk_index, 1.5), 2)
        FROM macro_dossier
        WHERE lower(headline) NOT LIKE '%book review:%'
          AND lower(headline) NOT LIKE '%the fed explained%'
        ORDER BY tail_risk_index DESC, alpha_score DESC, rowid DESC
        LIMIT ?;
        """, (limit - len(rows),)).fetchall()
        rows.extend(extra)

    for r in rows:
        con.execute("""
        INSERT OR REPLACE INTO m82_hud_dispatch_log (dossier_rowid, source, desk_cluster, dispatched_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP);
        """, (r[0], r[1], r[2]))

    con.commit()
    con.execute("PRAGMA wal_checkpoint(PASSIVE);")
    con.close()
    return rows

def patch_orch_burst():
    orch = BASE_DIR / "orch.py"
    if not orch.exists():
        return
    src = orch.read_text(encoding="utf-8", errors="ignore")
    # Forzar limite de lote/rafaga = 5 en cualquier bucle LIMIT 10 / range(10) / batch_size
    src_new = re.sub(r'(LIMIT\s+)10\b', r'\g<1>5', src, flags=re.IGNORECASE)
    src_new = re.sub(r'(batch_size\s*=\s*)\d+', r'\g<1>5', src_new)
    src_new = re.sub(r'(range\()10(\))', r'\g<1>5\g<2>', src_new)
    if src_new != src:
        orch.write_text(src_new, encoding="utf-8")
        print("[+] orch.py ajustado a ráfagas exactas de 5 tarjetas (BURST-5).")

def main():
    init_burst_state()
    patch_orch_burst()
    banner = get_live_banner()
    batch = pull_burst_batch(BURST_SIZE)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    print(f"=== M82 HUD BURST-5 DISPATCH :: {ts} ===")
    print(f"LIVE BANNER: {banner}")
    print("-" * 78)
    for idx, r in enumerate(batch, 1):
        clean_hl = re.sub(r"^\[[^\]]+\]\s*", "", r[3]).strip()
        print(f"[CARD {idx}/5 | #{r[0]:3d}] DESK={r[2]:22s} | A={r[4]:.2f} T={r[5]:.2f} | {clean_hl}")
    print("-" * 78)

    # Disparo inmediato del renderizador HUD / orch.py en modo rafaga de 5
    if (BASE_DIR / "orch.py").exists():
        subprocess.run(["pkill", "-f", "orch.py"], stderr=subprocess.DEVNULL)
        env = os.environ.copy()
        env["M82_BURST_SIZE"] = "5"
        lf = open(BASE_DIR / "logs" / "orch_burst5.log", "a")
        p = subprocess.Popen(["nohup", "python3", "-u", str(BASE_DIR / "orch.py")], stdout=lf, stderr=subprocess.STDOUT, env=env, start_new_session=True)
        print(f"[+] DISPARADOR BURST-5 ACTIVO EN SEGUNDO PLANO | orch.py PID={p.pid}")

if __name__ == "__main__":
    main()
