import sqlite3, os, json, datetime
BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
meta = {
  "ticker": "VENZ 2027",
  "price_jan": 0.16,
  "price_sep_warships": 0.30,
  "price_sep_current": 0.54,
  "total_bonds": 60_000_000_000,
  "total_interest": 40_000_000_000,
  "total_liabilities_est": "150-200B",
  "catalyst": "Trump warships + $50M bounty + Trump-Rodriguez UNGA debt overhaul Sep23",
  "rubio_quote": "Debt restructuring is key",
  "m82_q_tag": "Riesgo Short / Evaluar PQC",
  "risk": "CAC split + September court precedent winner + 3 hurdles freight/rehab/debt"
}
c.execute("INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json) VALUES (?,?,?,?,?,?,?,?)",
("M82_MACRO_FA_MAG","VEN_BONDS_SHORT_SQUEEZE","Trump Warships Trigger Rally in Venezuela Defaulted Bonds: VENZ 27 0.16 -> 0.54 highest since 2019", 99.2, 0.02, 1.5, 9.8, json.dumps(meta)))
c.execute("INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp) VALUES (?,?,?,?)",
("m82_geopolitical_events_daemon","VEN_BONDS_SHORT_SQUEEZE: 16c->54c rally","DISPATCHED", datetime.datetime.now().isoformat()))
conn.commit()
# verify
c.execute("SELECT id, risk_score, headline FROM macro_dosier WHERE category='VEN_BONDS_SHORT_SQUEEZE' ORDER BY id DESC LIMIT 1")
row = c.fetchone()
print(f"✅ CONFIRMADO: id={row[0]} risk={row[1]}")
print(f"   {row[2]}")
conn.close()
