import sqlite3

conn = sqlite3.connect("m82_database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO signals (source, category, asset_class, risk_score, headline, timestamp)
VALUES (?, ?, ?, ?, ?, datetime('now'))
""", (
    "M82_MACRO/M82 Wire",
    "FIXED_INCOME",
    "CORP_FLOATER",
    8.7,
    "XOM 2076 Floater SOFR-45bps puttable 2027 Texas Holdings Guarantee"
))

conn.commit()
conn.close()
print("✅ Señal XOM inyectada exitosamente en m82_database.db")
