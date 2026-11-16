
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
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
DB_PATH = BASE_DIR / "m82_database.db"
POST_DRAFT = BASE_DIR / "logs" / "m82_post_master_draft.md"
PER_DAEMON_LIMIT = 10

def get_live_banner():
    try:
        con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, timeout=15.0)
        r = con.execute("SELECT merey16_price, wti_price, wti_chg_pct, brent_price, brent_chg_pct FROM m82_live_market_quotes WHERE id=1").fetchone()
        con.close()
        if r:
            return _m82_live_banner()
    except Exception:
        pass
    return _m82_live_banner()

def extract_10_per_daemon():
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, timeout=60.0)
    # Selecciona hasta 10 titulares distintos por cada daemon/fuente activa en macro_dossier
    rows = con.execute("""
    WITH clean_dedup AS (
        SELECT
            rowid,
            UPPER(TRIM(source)) AS daemon_src,
            COALESCE(desk_cluster, 'QUANT_TELEMETRY_CORE') AS desk,
            TRIM(headline) AS raw_hl,
            ROUND(COALESCE(alpha_score, 1.0), 2) AS alpha,
            ROUND(COALESCE(tail_risk_index, 1.5), 2) AS tail_risk,
            ROUND(COALESCE(sentiment, 0.0), 2) AS sent,
            ROW_NUMBER() OVER (
                PARTITION BY UPPER(TRIM(source)), substr(TRIM(headline), 1, 65)
                ORDER BY rowid DESC
            ) AS dup_rn
        FROM macro_dossier
        WHERE lower(headline) NOT LIKE '%book review:%'
          AND lower(headline) NOT LIKE '%the fed explained%'
          AND lower(headline) NOT LIKE '%rachel maddow%'
    ),
    ranked_per_daemon AS (
        SELECT
            rowid, daemon_src, desk, raw_hl, alpha, tail_risk, sent,
            ROW_NUMBER() OVER (
                PARTITION BY daemon_src
                ORDER BY rowid DESC
            ) AS daemon_rn
        FROM clean_dedup
        WHERE dup_rn = 1
    )
    SELECT daemon_src, daemon_rn, rowid, desk, alpha, tail_risk, sent, raw_hl
    FROM ranked_per_daemon
    WHERE daemon_rn <= ?
    ORDER BY daemon_src ASC, daemon_rn ASC;
    """, (PER_DAEMON_LIMIT,)).fetchall()
    con.close()
    return rows

def patch_orch_burst10():
    orch = BASE_DIR / "orch.py"
    if not orch.exists():
        return
    src = orch.read_text(encoding="utf-8", errors="ignore")
    src_new = re.sub(r'(LIMIT\s+)5\b', r'\g<1>10', src, flags=re.IGNORECASE)
    src_new = re.sub(r'(batch_size\s*=\s*)\d+', r'\g<1>10', src_new)
    src_new = re.sub(r'(range\()5(\))', r'\g<1>10\g<2>', src_new)
    if src_new != src:
        orch.write_text(src_new, encoding="utf-8")

def main():
    patch_orch_burst10()
    banner = get_live_banner()
    rows = extract_10_per_daemon()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    grouped = {}
    for r in rows:
        grouped.setdefault(r[0], []).append(r)

    md_lines = [
        f"# M82 SOVEREIGN INTELLIGENCE DOSSIER :: BURST-10 PER DAEMON ({ts})",
        f"**Live Telemetry:** `{banner}` | **Governance:** `BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK`",
        f"**Total Daemons Activos en Muestra:** `{len(grouped)}` | **Total Vectores Extraídos:** `{len(rows)}`",
        ""
    ]

    print(f"=== M82 BURST-10 PER DAEMON :: {ts} ===")
    print(f"LIVE BANNER : {banner}")
    print(f"DAEMONS     : {len(grouped)} | TOTAL VECTORES: {len(rows)}")
    print("=" * 82)

    for daemon, items in grouped.items():
        avg_a = sum(x[4] for x in items) / len(items)
        avg_t = sum(x[5] for x in items) / len(items)
        print(f"\n>>> DAEMON: {daemon} (n={len(items)}/10 | Avg Alpha={avg_a:.2f} | Avg Tail-Risk={avg_t:.2f})")
        md_lines.append(f"## DAEMON: `{daemon}` (`n={len(items)}` | Avg Alpha: `{avg_a:.2f}` | Avg Tail-Risk: `{avg_t:.2f}`)")
        for item in items:
            _, rn, rowid, desk, alpha, tail, sent, raw_hl = item
            clean_hl = re.sub(r"^\[[^\]]+\]\s*", "", raw_hl).strip()
            print(f"  [{rn:2d}/10 | #{rowid:3d}] {desk:20s} | A={alpha:.2f} T={tail:.2f} | {clean_hl[:92]}")
            md_lines.append(f"- **[{rn:02d}/10 | #{rowid}]** (`{desk}` | `Alpha={alpha:.2f}` | `Tail={tail:.2f}` | `Sent={sent:+.2f}`): {clean_hl}")
        md_lines.append("")

    POST_DRAFT.parent.mkdir(parents=True, exist_ok=True)
    POST_DRAFT.write_text("\n".join(md_lines), encoding="utf-8")
    print("\n" + "=" * 82)
    print(f"[+] DOSSIER CONSOLIDADO PARA PUBLICACION GUARDADO EN: {POST_DRAFT}")

    if (BASE_DIR / "orch.py").exists():
        subprocess.run(["pkill", "-f", "orch.py"], stderr=subprocess.DEVNULL)
        env = os.environ.copy()
        env["M82_BURST_SIZE"] = "10"
        env["M82_PER_DAEMON"] = "10"
        lf = open(BASE_DIR / "logs" / "orch_burst10.log", "a")
        p = subprocess.Popen(["nohup", "python3", "-u", str(BASE_DIR / "orch.py")], stdout=lf, stderr=subprocess.STDOUT, env=env, start_new_session=True)
        print(f"[+] ORCHESTRADOR HUD REINICIADO EN MODO BURST-10 PER DAEMON | orch.py PID={p.pid}")

if __name__ == "__main__":
    main()
