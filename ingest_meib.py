#!/usr/bin/env python3
import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur = conn.cursor()

# 1. Asentamiento en macro_dossier
cur.execute("""
    INSERT OR REPLACE INTO macro_dossier (source, category, headline, risk_score, m82_tag, alpha_score)
    VALUES (
        'MEIB_CORPORATE_DOSSIER',
        'INVESTMENT_BANKING_PLATFORM',
        'Molina Energy Investment Banking (MEIB): Cross-border platform (Nashville TN & Caracas VZ via Corp Int JMM). Private credit, M&A, mezzanine, Quad-SPV origination. Legacy Kidder Peabody / NationsBank model.',
        1.68,
        'MEIB_NASHVILLE_CARACAS_HUB',
        0.99
    )
""")

# 2. Registración en m82_multi_stream
cur.execute("""
    INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
    VALUES (
        'MEIB_ORIGINATION_DESK',
        '[MEIB | NASHVILLE-CARACAS] Molina Energy Investment Banking platform synced — Origination engine via Corporación Internacional JMM, C.A. — Quad-SPV Syndication Active',
        'PROCESSED',
        0.99,
        'ENERGY_CROSS_BORDER_CREDIT',
        'MEIB_PROFILE_INGEST'
    )
""")

conn.commit()
conn.close()
print("✅ [MEIB INGEST] Perfil institucional de MEIB/JMM integrado en m82_database.db.")
