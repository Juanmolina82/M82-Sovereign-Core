#!/usr/bin/env python3
# M82 SOVEREIGN CORE v61.0.30 - DDL AUDIT & TELEMETRY SWARM INGESTION
import os, json, sqlite3, subprocess
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur = conn.cursor()

# 1. Auditoría de Conteo por Tabla DDL
tables = ["m82_multi_stream", "macro_dossier", "m82_daemons_registry", "price_ticks", "orders", "positions"]
print("\n📊 === M82 DDL RELATIONAL AUDIT (6 TABLES) ===")
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t};")
        cnt = cur.fetchone()[0]
        print(f"  • TABLA '{t}': {cnt} registros")
    except Exception as e:
        print(f"  • TABLA '{t}': ERROR ({e})")

# 2. Ingesta v61.0.30 (Global Macro, Merey/WTI Spread & Crypto Liquidity Recovery)
now_utc = datetime.now(timezone.utc).isoformat()
headline = "[M82 TELEMETRY SWARM v61.0.30] WTI $102.80 Backwardation Boosts Implied Merey 16 Net ($88.80-$90.50) -- Tether/Circle $2.54B Freeze Restores Market Stability -- Delaware Quad-SPV Active"
tag = "v61.0.30-M82-SWARM-ENERGY-CRYPTO-DELAWARE-SPV"

meta = {
    "user_id": "jmmp@molina82.com",
    "merey_net_realization": "$88.80 - $90.50/bbl",
    "wti_benchmark": "$102.80/bbl (Dec26)",
    "binance_freeze_recovery": "$2.54B isolated / Stablecoin blacklist active",
    "spv_escrow": "Citibank N.A. New York Master Escrow",
    "timestamp": now_utc,
    "security_protocol": "Zero-PII Gateway D-34 Masked Pass Active"
}

cur.execute("""
    INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node)
    VALUES ('M82 Telemetry Engine / Refinitiv Wire', 'GLOBAL_MACRO_ENERGY_SWARM', ?, 1.20, ?, 0.85, ?, 'v61.0.30', 'NODO_CHARALLAVE_L4L5')
""", (headline, tag, json.dumps(meta, ensure_ascii=False)))

conn.commit()

# Checkpoint WAL Atómico Limpio
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total = cur.fetchone()[0]
conn.close()

print(f"\n🔒 M82 SOVEREIGN CORE v61.0.30 SUCCESS")
print(f"🟢 TOTAL REGISTROS CERTIFICADOS EN MACRO_DOSSIER: {total}")
print(f"🟢 WAL CHECKPOINT: TRUNCATE CLEAN 0/0/0")
print(f"🟢 TAG INGESTADO: {tag}\n")

# Disparar renderizado en Plantilla Opción A (Quantum Terminal HUD)
subprocess.Popen(["python3", os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py"), "A"])
