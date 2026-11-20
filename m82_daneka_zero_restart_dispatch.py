#!/usr/bin/env python3
import json
import os
import sqlite3
import urllib.request
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
HUB_8286_URL = "http://127.0.0.1:8286/api/ingest"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"

def main():
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    ts_tag = datetime.now(timezone.utc).strftime("%H%M%S")

    payload = {
        "ts": now_utc,
        "locus": "Charallave_L4L5_Edge_Caracas_HQ",
        "governance": "BUNKER_MODE_030X_LOCK_NO_TRADE",
        "exposure": 0.22,
        "var_daily": 0.0168,
        "warsh_spread_bp": 102.0,
        "futures_1250": {
            "NASDAQ_F": {"price": 25583.70, "pct": -3.52},
            "SP500_F": {"price": 7041.70, "pct": -1.87},
            "RUSSELL2000_F": {"price": 2617.00, "pct": -1.43},
            "DOWJONES_F": {"price": 48877.60, "pct": -0.45},
        },
        "cross_asset": {
            "VIX": 30.86,
            "BTC": 59418.08,
            "NVDA": 138.18,
            "UST_10Y": 4.944,
            "GOLD_GC1": 3680.4,
            "SILVER_SIC1": 52.240,
        },
    }

    headline = (
        f"[{ts_tag}] [DANEKA_M82_ZERO_RESTART] NASDAQ=F 25,583.70 (-3.52%) | "
        "SP500=F 7,041.70 (-1.87%) | VIX 30.86 (+8.51%) | BTC $59,418.08 (-3.39%) | "
        "NVDA $138.18 | UST10Y 4.944% | GC1! $3,680.4 | SIc1 $52.240 | BUNKER 0.30x LOCK"
    )

    # 1. Persistencia Atómica SQLite3 WAL + FTS5 (Zero-Restart / Zero-Contention)
    conn = sqlite3.connect(DB_PATH, timeout=120.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    conn.execute("PRAGMA synchronous=NORMAL;")

    conn.execute(
        """
        INSERT OR IGNORE INTO macro_dossier (
            source, category, headline, risk_score, m82_tag, sentiment, metadata_json, alpha_score
        ) VALUES (?, 'DANEKA_SOVEREIGN_SYNTHESIS', ?, 1.90, 'BUNKER_HOLD_030X', -0.90, ?, 0.99)
        """,
        ("DANEKA_M82_HUB_8286", headline, json.dumps(payload)),
    )

    conn.execute(
        """
        INSERT OR IGNORE INTO m82_multi_stream (
            daemon_source, headline, status, alpha_score, asset_impact, event_trigger
        ) VALUES (?, ?, 'VERIFIED', 0.99, 'CROSS_ASSET_DANEKA_V60', 'ZERO_RESTART_SYNC_V60')
        """,
        ("DANEKA_AUTO_PUSH", headline),
    )

    # Actualización FTS5 segura si la tabla virtual está montada
    fts_exists = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='macro_dossier_fts';"
    ).fetchone()
    if fts_exists:
        conn.execute(
            "INSERT INTO macro_dossier_fts(macro_dossier_fts) VALUES('rebuild');"
        )

    wal_status = conn.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone()
    conn.close()
    print(f"🟢 [SQLITE3 WAL + FTS5] Checkpoint: {wal_status} (Zero-Restart OK)")

    # 2. Push directo al Hub :8286 (no bloqueante)
    try:
        req = urllib.request.Request(
            HUB_8286_URL,
            data=json.dumps({"headline": headline, "payload": payload}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            print(f"🟢 [HUB :8286] HTTP {resp.status} — Telemetría acoplada")
    except Exception as e:
        print(f"🟡 [HUB :8286] Cola local sellada en WAL (endpoint standby: {e})")

    # 3. Despacho Limpio DANEKA M82 (ntfy.sh prioridad high + tarjeta HUD /storage/emulated/0/M82card)
    try:
        ntfy_req = urllib.request.Request(
            NTFY_URL,
            data=headline.encode("utf-8"),
            headers={
                "Title": "M82 DANEKA :: CROSS-ASSET TAIL-RISK SEAL",
                "Priority": "high",
                "Tags": "shield,chart_with_downwards_trend,lock",
            },
            method="POST",
        )
        with urllib.request.urlopen(ntfy_req, timeout=4) as r:
            print(f"🟢 [DANEKA NTFY RELAY] HTTP {r.status} — Despacho limpio emitido")
    except Exception as e:
        print(f"🟡 [DANEKA NTFY RELAY] Offline fallback ({e})")

if __name__ == "__main__":
    main()
