import os, datetime, sqlite3
output_dir = os.path.expanduser('~/M82')
db_path = os.path.join(output_dir, 'm82_database.db')
bac_data = {"RIC": "BAC.N","Name": "Bank of America","Sector": "BANKS","Spot": 42.15,"Target": 48.00,"PE": 13.2,"Consensus": "Buy","Upside_%": 13.88,"Alpha": 0.94,"Timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S VET'),"Source": "LSEG Workspace jmmp@molina82.com"}
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA journal_mode=WAL;"); conn.execute("PRAGMA busy_timeout=60000;")
conn.execute("INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, sentiment, asset_impact, event_trigger) VALUES (?,?,?,?,?,?,?)",('REFINITIV_BAC.N', f'[WALLSTREET MASTER | BAC.N] Bank of America Spot ${bac_data["Spot"]} Target ${bac_data["Target"]} Upside {bac_data["Upside_%"]:.1f}% | {bac_data["Consensus"]}', 'PROCESSED', 0.94, 0.85, 'BANKS', f'LSEG_BAC.N_MASTER_{datetime.datetime.now().strftime("%Y%m%d")}'))
conn.commit(); conn.execute("PRAGMA wal_checkpoint(TRUNCATE);"); conn.close()
print(f"BAC_METRICS_SUCCESS: Telemetría BAC.N inyectada en WAL m82_database.db")
