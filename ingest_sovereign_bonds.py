#!/usr/bin/env python3
import os, sqlite3, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

# Matriz extraída de Refinitiv Workspace (Imagen 1000277614.jpg)
BONDS_DATA = [
    # Ticker, Last, Bid, Ask, Chg1D, ChgWTD, ChgYTD, Type
    ("VENZ_13.625_2018", 58.908, 58.278, 59.537, -0.10, -2.24, 79.26, "SOVEREIGN"),
    ("VENZ_7.000_2018",  44.560, 44.172, 44.947, -0.08, -3.08, 64.60, "SOVEREIGN"),
    ("VENZ_7.750_2019",  49.136, 48.719, 49.552, -0.27, -3.19, 83.67, "SOVEREIGN"),
    ("VENZ_6.000_2020",  43.201, 42.775, 43.628, -0.32, -3.36, 61.00, "SOVEREIGN"),
    ("VENZ_12.75_2022",  57.984, 57.528, 58.440, -0.09, -2.63, 79.80, "SOVEREIGN"),
    ("VENZ_9.000_2023",  50.157, 49.719, 50.595, -0.27, -2.58, 76.92, "SOVEREIGN"),
    ("VENZ_8.250_2024",  49.522, 49.064, 49.980, -0.37, -3.00, 74.82, "SOVEREIGN"),
    ("VENZ_7.650_2025",  48.695, 48.254, 49.135, -0.46, -3.13, 71.15, "SOVEREIGN"),
    ("VENZ_11.75_2026",  57.233, 56.744, 57.722, -0.56, -2.88, 74.94, "SOVEREIGN"),
    ("VENZ_9.250_2027",  51.953, 51.577, 52.329, -0.59, -3.16, 58.35, "SOVEREIGN"),
    ("VENZ_9.250_2028",  51.696, 51.315, 52.077, -0.40, -3.42, 61.72, "SOVEREIGN"),
    ("VENZ_11.95_2031",  56.776, 56.343, 57.172, -0.42, -3.51, 0.00,  "SOVEREIGN"),
    ("VENZ_9.375_2034",  51.657, 51.291, 52.023, -0.33, -3.23, 57.10, "SOVEREIGN"),
    ("VENZ_7.000_2038",  44.939, 44.560, 45.317, -0.58, -3.92, 51.81, "SOVEREIGN"),
    ("PDVSA_8.50_2020", 115.315, 114.944,115.686, -0.03,  0.16, 14.08, "PDVSA"),
    ("PDVSA_9.00_2021",  46.295, 45.900, 46.689,  0.02, -2.83, 81.45, "PDVSA"),
    ("PDVSA_6.00_2022",  38.014, 37.613, 38.414,  0.04, -2.78, 84.95, "PDVSA"),
    ("PDVSA_12.75_2022", 52.287, 51.868, 52.706,  2.22, -1.82, 82.61, "PDVSA"),
    ("PDVSA_6.00_2024",  39.679, 39.374, 39.984,  0.13, -2.65, 68.04, "PDVSA"),
    ("PDVSA_6.00_2026",  39.692, 39.339, 40.044, -0.09, -2.72, 68.12, "PDVSA"),
    ("PDVSA_5.375_2027", 38.491, 38.093, 38.889,  1.14, -3.00, 63.01, "PDVSA"),
    ("PDVSA_9.75_2035",  47.840, 47.413, 48.267, -0.08, -2.96, 83.25, "PDVSA"),
    ("PDVSA_5.50_2037",  38.620, 38.242, 38.997,  0.24, -2.56, 64.86, "PDVSA")
]

def run_ingest():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    cur = conn.cursor()
    
    # 1. Asentar en price_ticks
    for ticker, last_p, bid, ask, d1, wtd, ytd, btype in BONDS_DATA:
        cur.execute("""
            INSERT OR REPLACE INTO price_ticks (asset, bid, ask, last_price, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (ticker, bid, ask, last_p))
    
    # 2. Registrar evento telemétrico de la matriz de bonos
    ts = datetime.datetime.now().strftime("%H:%M:%S ET")
    headline = f"[{ts}] REFINITIV BOND MATRIX: 23 Bonos Soberanos/PDVSA Ingestados — PDVSA20 $115.31 | VENZ34 $51.65 | VENZ26 $57.23 | PDVSA26 $39.69"
    cur.execute("""
        INSERT OR IGNORE INTO m82_multi_stream 
        (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
        VALUES ('REFINITIV_BOND_WORKSPACE', ?, 'PENDING', 0.99, 'SOVEREIGN_DEBT', 'REFINITIV_MATRIX_SYNC')
    """, (headline,))
    
    conn.commit()
    conn.close()
    print(f"✅ [SUCCESS] 23 Bonos Soberanos/PDVSA inyectados en ~/M82/m82_database.db")

if __name__ == "__main__":
    run_ingest()
