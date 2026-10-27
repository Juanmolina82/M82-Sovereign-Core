import sqlite3, os, sys
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def arm_breakout_trigger():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA busy_timeout=60000;")
    cursor = conn.cursor()

    # 1. Crear tabla de parámetros para la orden condicional
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS m82_execution_triggers (
        trigger_id TEXT PRIMARY KEY,
        asset_cluster TEXT,
        target_support_level REAL,
        status TEXT,
        armed_timestamp DATETIME,
        execution_window TEXT
    );
    """)

    # 2. Registrar el gatillo de corto condicionado al soporte 0.00%
    cursor.execute("""
    INSERT OR REPLACE INTO m82_execution_triggers 
    VALUES (
        'JPM_BREAKOUT_SHORT_01',
        'GLOBAL_BANKS_USGC',
        0.00,
        'ARMED_AWAITING_JPM_BMO',
        datetime('now'),
        '2026-10-13 06:45:00'
    );
    """)

    # 3. Asentar en la multiseñal WAL la gobernanza de ejecución
    cursor.execute("""
    INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
    VALUES (
        'EXECUTION_GOVERNANCE',
        '[TRIGGER ARMED] SHORT conditional on 0.00% support break POST-JPM BMO | Night trades LOCKED',
        'ACTIVE',
        0.99,
        'GLOBAL_BANKS'
    );
    """)

    conn.commit()
    conn.close()
    print("=========================================================================")
    print("🛡️  M82 EXECUTION TRIGGER ARMED — CHARALLAVE EDGE L4")
    print("=========================================================================")
    print(" 🛑 Estado Noche     : NO RE-ENTRADAS / BUNKER 0.30x LOCK")
    print(" 🎯 Gatillo Corto    : Ruptura confirmada de nivel 0.00% de Refinitiv Workspace")
    print(" ⏰ Ventana Objetivo : Post-JPMorgan Chase BMO (Mañana 06:45 AM VET)")
    print("=========================================================================")

if __name__ == '__main__':
    arm_breakout_trigger()
