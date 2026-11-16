#!/usr/bin/env python3
"""
M82 UNIFIED INTEL PIPELINE (SIN DUPLICAR AGENTES)
Conecta LSEG Bridge -> macro_dossier (App 8282) -> Telegram & ntfy Push
"""
import os
import time
import sqlite3
import urllib.request
import urllib.parse
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
DB_PATH = BASE_DIR / "m82_database.db"
TG_TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
TG_CHAT = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"

def get_db():
    con = sqlite3.connect(str(DB_PATH), timeout=60.0)
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA busy_timeout=60000;")
    return con

def ensure_tracking_column(con):
    cols = [r[1] for r in con.execute("PRAGMA table_info(macro_dossier);").fetchall()]
    if "dispatched_tg" not in cols:
        con.execute("ALTER TABLE macro_dossier ADD COLUMN dispatched_tg INTEGER DEFAULT 0;")
        con.commit()

def push_telegram(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": TG_CHAT, "text": text, "parse_mode": "Markdown"}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status == 200

def push_ntfy(title, body):
    req = urllib.request.Request(
        NTFY_URL,
        data=body.encode("utf-8"),
        headers={"Title": title, "Priority": "high", "Tags": "satellite,shield"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status in (200, 204)

def sync_and_broadcast():
    con = get_db()
    ensure_tracking_column(con)
    cur = con.cursor()

    # 1. Promover eventos nuevos de m82_multi_stream (LSEG / Desks) hacia macro_dossier (App 8282)
    pending = cur.execute("""
        SELECT rowid, daemon_source, headline, alpha_score, asset_impact
        FROM m82_multi_stream
        WHERE status = 'PENDING' AND alpha_score >= 0.70
        ORDER BY rowid DESC LIMIT 10
    """).fetchall()

    for rid, src, hl, alpha, asset in pending:
        cur.execute("""
            INSERT INTO macro_dossier (node_origin, governance_mode, var_daily, active_exposure, source, category, desk_cluster, headline, risk_score, m82_tag, sentiment, alpha_score, tail_risk_index, dispatched_tg)
            VALUES ('NODO_CHARALLAVE_EDGE', 'BUNKER_MODE_0.30x_LOCK', 1.68, 0.22, ?, 'AUTO_SWARM_INTEL', ?, ?, ?, 'M82_AUTO_V60', 0.0, ?, 1.50, 0)
        """, (src, asset or "GLOBAL_MACRO_DESK", hl, alpha, alpha))
        cur.execute("UPDATE m82_multi_stream SET status = 'SYNCED_DOSSIER' WHERE rowid = ?", (rid,))

    con.commit()

    # 2. Despachar a Telegram + ntfy todo nuevo vector en macro_dossier aun no notificado
    unsent = cur.execute("""
        SELECT rowid, source, desk_cluster, risk_score, alpha_score, headline
        FROM macro_dossier
        WHERE COALESCE(dispatched_tg, 0) = 0
        ORDER BY rowid ASC LIMIT 5
    """).fetchall()

    for rid, src, desk, risk, alpha, hl in unsent:
        now_et = datetime.now().strftime("%H:%M:%S")
        msg = (
            f"📡 *#M82 MACRO DOSSIER ALERT* :: `{now_et}`\n"
            f"───────────────────────────\n"
            f"🏛 *Desk:* `{desk}` | *Fuente:* `{src}`\n"
            f"📊 *Risk:* `{risk:.2f}` | *Alpha:* `{alpha:.2f}`\n"
            f"📰 *Vector:* {hl}\n"
            f"───────────────────────────\n"
            f"🔒 *BUNKER 0.30x LOCK* (Exp `0.22x` | VaR `1.68%`)"
        )
        try:
            if push_telegram(msg):
                push_ntfy(f"M82 [{desk}] Risk {risk:.2f}", hl[:240])
                cur.execute("UPDATE macro_dossier SET dispatched_tg = 1 WHERE rowid = ?", (rid,))
                con.commit()
                print(f"[{now_et}] [+] Sincronizado App 8282 + Telegram rowid={rid}")
        except Exception as e:
            print(f"[!] Error despacho rowid={rid}: {e}")

    con.close()

if __name__ == "__main__":
    print("=== M82 AUTO INTEL PIPELINE ACTIVO (60s LOOP) ===")
    while True:
        try:
            sync_and_broadcast()
        except Exception as ex:
            print(f"[!] Ciclo pipeline: {ex}")
        time.sleep(60)
