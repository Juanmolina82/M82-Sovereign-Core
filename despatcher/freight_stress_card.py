import pathlib, os
from dotenv import load_dotenv
load_dotenv(dotenv_path=pathlib.Path.home()/ 'M82/.env')
import sqlite3
db = pathlib.Path.home()/ 'M82/m82_database.db'
conn = sqlite3.connect(db)
conn.execute("PRAGMA busy_timeout=120000;")
conn.execute("INSERT INTO m82_multi_stream (daemon_source, event_trigger, headline) VALUES (?,?,?)",
             ('M82_HUD_DISPATCHER','FREIGHT_STRESS_HUD_20261022','HUD CARD: BAB-EL-MANDEB BLOCK Ton-Mile +18-24% — Bunker 0.30x LOCK — VaR 1.68% — WAL 0/0/0 — Image M82_V60_AGI_FREIGHT_STRESS_BAB-EL-MANDEB_BLOCK.png dispatched to PWA :8080 — TECHNICAL_ONLY_NDA'))
conn.commit()
conn.close()
print("🚀 HUD CARD DESPACHADA @ PWA Surface :8080 — http://localhost:8080/assets/M82_V60_AGI_FREIGHT_STRESS_BAB-EL-MANDEB_BLOCK.png")
print("🔒 Telemetría Confidencial bajo BUNKER 0.30x LOCK — NO X PUBLIC")
