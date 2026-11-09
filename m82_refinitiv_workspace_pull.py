#!/usr/bin/env python3
import sqlite3, os, csv, datetime

USER_EMAIL="jmmp@molina82.com"
DB=os.path.expanduser("~/M82/m82_database.db")
CSV=os.path.expanduser("~/M82/refinitiv_export.csv")

def load_csv():
    if not os.path.exists(CSV):
        print(f"[ERROR M82] No se localizó el archivo: {CSV}")
        print("[INSTRUCCIÓN WORKSPACE] En Workspace (jmmp@molina82.com): Watchlist M82 100+ -> Export -> CSV -> Guardar en ~/M82/refinitiv_export.csv")
        return {}
    data={}
    with open(CSV, newline='', encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        print(f"[CSV WORKSPACE] Encabezados detectados: {reader.fieldnames}")
        for row in reader:
            ric = row.get("RIC") or row.get("Instrument") or row.get("Ticker") or row.get("Symbol") or ""
            ric = ric.strip()
            if not ric:
                continue
            price_str = row.get("Price") or row.get("Last") or row.get("TRDPRC_1") or row.get("Close") or "0"
            chg_str = row.get("Change%") or row.get("% Change") or row.get("Change") or row.get("PCTCHG") or "0"
            try:
                price=float(str(price_str).replace(",","").replace("$","").replace("%","") or 0)
                chg=float(str(chg_str).replace(",","").replace("%","") or 0)
            except:
                continue
            if price == 0:
                print(f"[SKIP STRICT] {ric} posee precio 0.00 — Inyección cancelada.")
                continue
            data[ric] = {"price": price, "chg_pct": chg}
    print(f"[CSV OK] {len(data)} activos procesados con precios REALES. Ceros sellados: 0.")
    return data

def ingest(data):
    if not data:
        print("[M82 GOVERNANCE] SIN DATOS REALES VALIDADOS — La base de datos no fue modificada.")
        return
    con=sqlite3.connect(DB, timeout=60.0)
    cur=con.cursor()
    cur.execute("PRAGMA busy_timeout=60000;")
    cur.execute("PRAGMA journal_mode=WAL;")
    ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO macro_dossier(source,category,headline,risk_score,m82_tag,sentiment) VALUES(?,?,?,?,?,?)",
    (f"REFINITIV_WORKSPACE_{USER_EMAIL}", "WALL_STREET_100_FULL_UNIVERSE",
     f"Refinitiv Pull REAL {len(data)} activos - Sin ceros - {ts}", 1.50, "M82_WALLSTREET_FULL_PULL", 0.50))
    for ric, vals in data.items():
        symbol=ric.replace(".","_").replace("-","_").replace("=","_").replace(":","_")
        cur.execute("INSERT OR REPLACE INTO m82_global_derivatives (symbol, contract_name, asset_class, spot_price, daily_change, pct_change, rsi_14d, val_alpha) VALUES(?,?,?,?,?,?,?,?)",
        (symbol, ric, "WALL_STREET", vals["price"], vals["chg_pct"], vals["chg_pct"], 50.0, 0.95))
    con.commit()
    chk=cur.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone()
    print(f"[M82 OK] ✅ {len(data)} activos sellados con éxito. WAL Engine: {chk}")
    con.close()

if __name__=="__main__":
    data=load_csv()
    ingest(data)
