import os, sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA busy_timeout=60000;")
conn.execute("PRAGMA journal_mode=WAL;")

# Configuración de bypass táctico para fuentes críticas
cur = conn.cursor()
cur.execute("""
    UPDATE m82_multi_stream 
    SET status = 'PENDING' 
    WHERE daemon_source IN ('CHEVRON_JV', 'CITGO_OFAC_DESK') 
      AND alpha_score >= 0.85 
      AND status = 'DISCARDED';
""")
conn.commit()
print(f"🟢 [M82 ALPHA BYPASS] Registros rehabilitados: {cur.rowcount}")
conn.close()
