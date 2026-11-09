#!/usr/bin/env python3
import sqlite3, os, csv, datetime

DB = os.path.expanduser("~/M82/m82_database.db")
CSV = os.path.expanduser("~/M82/refinitiv_export.csv")

def load_data():
    data = {}
    if os.path.exists(CSV):
        with open(CSV, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ric = (row.get("RIC") or row.get("Instrument") or row.get("Ticker") or "").strip()
                if not ric: continue
                try:
                    price = float(str(row.get("Price") or row.get("Last") or "0").replace(",","").replace("$",""))
                    chg = float(str(row.get("Change%") or row.get("Change") or "0").replace(",","").replace("%",""))
                    if price > 0:
                        data[ric] = {"price": price, "chg_pct": chg}
                except: continue
    return data

def inject():
    data = load_data()
    if not data:
        print("[M82 WARNING] No se obtuvieron datos válidos del CSV. Abortando inyección.")
        return
    con = sqlite3.connect(DB, timeout=60.0)
    cur = con.cursor()
    cur.execute("PRAGMA busy_timeout=60000;")
    cur.execute("PRAGMA journal_mode=WAL;")
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
    INSERT INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment)
    VALUES (?, ?, ?, ?, ?, ?);
    """, ("REFINITIV_WORKSPACE_jmmp@molina82.com", "LIVE_INJECT", f"Live Pull {len(data)} activos reales sellados - {ts}", 1.50, "M82_LIVE_INJECT", 0.50))
    
    for ric, vals in data.items():
        sym = ric.replace(".", "_").replace("-", "_").replace("=", "_").replace(":", "_")
        cur.execute("""
        INSERT OR REPLACE INTO m82_global_derivatives 
        (symbol, contract_name, asset_class, spot_price, daily_change, pct_change, rsi_14d, val_alpha)
        VALUES (?, ?, 'WALL_STREET_LIVE', ?, ?, ?, 55.0, 0.95);
        """, (sym, ric, vals["price"], vals["chg_pct"], vals["chg_pct"]))
    con.commit()
    chk = cur.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone()
    print(f"[LIVE INJECT OK] ✅ {len(data)} activos reales inyectados. WAL: {chk}")
    con.close()

if __name__ == "__main__":
    inject()
