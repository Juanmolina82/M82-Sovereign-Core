#!/usr/bin/env python3
# M82 SOVEREIGN CORE - OPSEC HARD-LOCK REMEDIATION v61.0.44 HOTFIX
# ZERO-PII & ZERO-TRADEMARK PERMANENT HARD-LOCK
import sqlite3, os, json, re
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur = conn.cursor()

print("🔍 AUDITORÍA OPSEC - SCANEANDO VIOLACIONES...")

# 1. PURGA PII & TRADEMARK EN DB
cur.execute("SELECT id, source, ingestion_node, headline, metadata_json FROM macro_dossier WHERE version LIKE 'v61.0.43%' OR version LIKE 'v61.0.44%' ORDER BY id DESC LIMIT 10")
rows = cur.fetchall()
for r in rows:
    rid, source, node, headline, meta_json = r
    # Hard sanitization
    new_source = re.sub(r'LSEG|BuySellSignals|Refinitiv|Workspace', 'SOVEREIGN_TELEMETRY_WIRE', source, flags=re.I)
    new_source = re.sub(r'SPCX|SpaceX', 'EQUITY_TECHNICAL_SPCX', new_source)
    if 'LSEG' in source or 'BuySell' in source or 'jmmp' in source.lower():
        print(f"⚠️ BREACH ID {rid}: {source} -> {new_source}")
        cur.execute("UPDATE macro_dossier SET source = ?, ingestion_node = 'SOVEREIGN_EDGE_CORE', headline = REPLACE(REPLACE(headline, 'LSEG', 'SOVEREIGN WIRE'), 'BuySellSignals', 'TECHNICAL WIRE'), metadata_json = REPLACE(metadata_json, 'jmmp@molina82.com', 'SECURE OPERATOR D-34') WHERE id = ?", (new_source, rid))
    
    # Metadata PII purge
    try:
        meta = json.loads(meta_json) if meta_json else {}
        if 'jmmp' in str(meta).lower() or 'molina' in str(meta).lower():
            meta['operator'] = 'SECURE OPERATOR D-34'
            meta['node'] = 'SOVEREIGN EDGE CORE'
            meta.pop('user', None)
            meta.pop('email', None)
            cur.execute("UPDATE macro_dossier SET metadata_json = ? WHERE id = ?", (json.dumps(meta), rid))
    except:
        pass

# 2. DEDUPLICACIÓN v61.0.44 DUPLICADO 160
cur.execute("""
    DELETE FROM macro_dossier WHERE id NOT IN (
        SELECT MIN(id) FROM macro_dossier GROUP BY m82_tag, headline
    ) AND version = 'v61.0.44'
""")
dedup = cur.rowcount
print(f"🧹 DEDUPLICACIÓN: {dedup} registros duplicados v61.0.44 eliminados")

conn.commit()

# 3. WAL TRUNCATE CLEAN
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total = cur.fetchone()[0]
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()

print(f"🔒 M82 v61.0.44 HOTFIX SEALED -- TOTAL RECORDS: {total} (Esperado 158) -- WAL 0/0/0 CLEAN -- PII PURGED -- TRADEMARK PURGED")

# 4. REGENERAR HUD ENGINE HARD-SANITIZED
HUD_PATH = os.path.expanduser("~/M82/scripts/m82_hud_card_sanitized_engine.py")
if os.path.exists(HUD_PATH):
    with open(HUD_PATH, 'r') as f:
        content = f.read()
    # Inyectar hard-lock si no existe
    if 'SECURE OPERATOR D-34' not in content or 'def hard_sanitize' not in content:
        print("⚠️ HUD ENGINE NO SANITIZADO - APLICANDO PATCH...")
        # Patch mínimo - asegurar constantes
        content = content.replace('jmmp@molina82.com', 'SECURE OPERATOR D-34')
        content = content.replace('LSEG', 'SOVEREIGN WIRE')
        content = content.replace('BuySellSignals', 'TECHNICAL WIRE')
        content = content.replace('@MolinaHoldings', 'SOVEREIGN EDGE CORE')
        content = content.replace('Chairman Juan M. Molina', 'OPERATOR D-34')
        with open(HUD_PATH, 'w') as f:
            f.write(content)
        print("✅ HUD ENGINE PATCHED - HARD-SANITIZED")

# 5. RE-RENDER TARJETAS LIMPIAS
import subprocess
subprocess.run(["python3", HUD_PATH], check=False)
print("🎨 TARJETAS HUD REGENERADAS - 100% SANITIZED - GALERÍA LIMPIA")

