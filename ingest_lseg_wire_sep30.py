import sqlite3, os, json, datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS macro_dosier (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
        source TEXT, 
        category TEXT, 
        headline TEXT, 
        gprk_index REAL, 
        yield_10y_delta REAL, 
        oil_spread_impact REAL, 
        risk_score REAL, 
        metadata_json TEXT
    )
''')

meta = {
  "pce_mom": 0.3, "pce_yoy": 3.4, "pce_expected": 0.4,
  "yield_2y": 4.868, "yield_10y": 5.272, "yield_30y": 5.6298,
  "spx": 7716.67, "nasdaq": 27071.20, "dow": 51379.94,
  "wti": 91.33, "brent": 103.71,
  "fed_keep_prob": 0.65,
  "source_url": "urn:newsml:newswire.refinitiv.com:20260930:nL6N45M0WZ:2"
}

c.execute("""
    INSERT INTO macro_dosier 
    (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "M82_MACRO_REUTERS_WIRE",
    "PCE_FED_REPRICING",
    "PCE 0.3% vs 0.4% exp dampens Fed hike odds; 2Y eases to 4.868% but 10Y at 5.272% biggest monthly gain since 2022",
    98.7, 0.017, 1.12, 9.7, json.dumps(meta)
))

conn.commit()
print("✅ M82_MACRO Wire Sep30 inyectado: PCE 0.3% / 10Y 5.272% / Brent $103.71")
conn.close()
