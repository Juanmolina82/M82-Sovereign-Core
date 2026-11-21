import os, sqlite3, pandas as pd

CSV_PATH = os.path.expanduser("~/M82/lseg_364_full.csv")
DB_PATH = os.path.expanduser("~/M82/m82_database.db")

if os.path.exists(CSV_PATH):
    try:
        df = pd.read_csv(CSV_PATH)
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA busy_timeout=60000;")
        
        # Ingesta masiva
        df.to_sql('lseg_364_master', conn, if_exists='replace', index=False)
        
        c = conn.cursor()
        c.execute("""
            CREATE VIEW IF NOT EXISTS usgc_leverage_score AS
            SELECT * FROM lseg_364_master
            WHERE Identifier IN ('AMTB.N', 'BPOP.OQ', 'WAL.N', 'TCBI.TXS');
        """)
        
        conn.commit()
        conn.close()
        print("✅ CSV LSEG 364 procesado con éxito. Módulos de scoring activos.")
    except Exception as e:
        print(f"⚠️ Error procesando CSV: {e}")
else:
    print("⏳ Esperando exportación de ~/M82/lseg_364_full.csv...")
