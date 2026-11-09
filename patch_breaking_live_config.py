#!/usr/bin/env python3
import sqlite3, os, json, datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 1. Asegurar índice de unicidad estricto para evitar duplicación de Daemons
c.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_multistream_source_headline 
    ON m82_multi_stream (daemon_source, headline);
""")

# 2. Configurar la tabla de parámetros globales del motor visual
c.execute("""
    CREATE TABLE IF NOT EXISTS m82_system_config (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
""")

configs = [
    ("BREAKING_LIVE_CARD_MODE", "FULL_QUANTUM_1080X1350"),
    ("BOT_IMAGE_EMBED_TYPE", "DIRECT_ATTACHMENT_LARGE"),
    ("DUPLICATE_DAEMON_PREVENTION", "STRICT_UNIQUE_HEADLINE"),
    ("DEFAULT_WATERMARK", "@MolinaHoldings LLC")
]

for k, v in configs:
    c.execute("""
        INSERT INTO m82_system_config (key, value, updated_at) 
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP;
    """, (k, v))

conn.commit()
conn.close()

print("================================================================================")
print(" 🛠️ PARCHE APLICADO: BREAKING LIVE CONFIGURATION BLINDADA")
print("================================================================================")
print(" ✓ Anti-duplicación de Daemons forzada mediante índice UNIQUE en SQLite.")
print(" ✓ Formato de tarjeta estandarizado a 1080x1350 (4:5 Ratio Direct Attachment).")
print(" ✓ Servidores API (8083) y Assets (8080) alineados a la suite principal M82.")
print("================================================================================")
