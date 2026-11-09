import os, datetime, sqlite3, pandas as pd

output_dir = os.path.expanduser('~/M82')
db_path = os.path.join(output_dir, 'm82_database.db')

event_data = {
    "Event": "US Strike Qeshm Island",
    "Location": "Strait of Hormuz / Persian Gulf",
    "Source": "WSJ / Refinitiv Wire",
    "Impact_Assets": "Brent, WTI, BDTI Index, Aframax TD25",
    "Status": "BUNKER MODE 0.30x LOCK ACTIVE",
    "Timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S VET')
}

conn = sqlite3.connect(db_path)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
conn.execute(
    "INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, sentiment, asset_impact, event_trigger) VALUES (?,?,?,?,?,?,?)",
    ('REFINITIV_HORMUZ_MONITOR', f'[HORMUZ LIVE] US Strikes Qeshm | Risk Premium Active | Merey $93.92 FOB Protected', 'PROCESSED', 0.98, 0.85, 'ENERGY_COMMODITIES', f'HORMUZ_LIVE_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}')
)
conn.commit()
conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()

print(f"HORMUZ_MONITOR_SUCCESS: Evento Qeshm asentado en WAL m82_database.db")
