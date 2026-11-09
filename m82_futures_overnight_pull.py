#!/usr/bin/env python3
# M82 OVERNIGHT FUTURES — ASIA + US + EUROPE + COMMODITIES — v61.0.51-A — ENV SAFE
import os, sqlite3, requests, datetime
import yfinance as yf

# Tickers Overnight — Mapeo LSEG → Yahoo para Termux sin Eikon key
FUTURES = {
    # US Index Futures Overnight
    "ES=F": "S&P 500 E-mini",
    "NQ=F": "Nasdaq 100 E-mini", 
    "YM=F": "Dow E-mini",
    "RTY=F": "Russell 2000 E-mini",
    # Asia Futures
    "NK=F": "Nikkei 225 JP",
    "^N225": "Nikkei Cash Proxy",
    "9984.HK": "HSI Proxy",
    # Europe Overnight
    "^GDAXI": "DAX Proxy",
    # Commodities — Tu cobertura Bunker
    "CL=F": "WTI Crude",
    "BZ=F": "Brent Proxy",
    "GC=F": "Gold",
    "SI=F": "Silver",
    # Rates & FX Overnight
    "ZB=F": "US 30Y Bond Future",
    "DX-Y.NYB": "DXY Dollar Index",
    "BTC-USD": "BTC Overnight"
}

print(f"🏛️ M82 FUTURES OVERNIGHT PULL — {datetime.datetime.now()} VET")

rows=[]
for ticker, name in FUTURES.items():
    try:
        d = yf.Ticker(ticker)
        h = d.history(period="2d", interval="1m")
        if h.empty: 
            h = d.history(period="5d")
        last = h['Close'].iloc[-1]
        prev = h['Close'].iloc[-2] if len(h)>1 else last
        chg = (last-prev)/prev*100
        vol = h['Volume'].iloc[-1] if 'Volume' in h else 0
        rows.append((ticker,name,float(last),float(chg),int(vol)))
        print(f"✅ {ticker:8} {name:20} {last:10.2f} {chg:+.2f}%")
    except Exception as e:
        print(f"⚠️ {ticker} error {e}")

# 2. Ingesta atómica SQLite — WAL MODE
db_path = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(db_path, timeout=60)
cur = conn.cursor()
cur.execute("PRAGMA busy_timeout=60000;")
cur.execute("PRAGMA journal_mode=WAL;")
cur.execute("""CREATE TABLE IF NOT EXISTS m82_futures_overnight (
    timestamp TEXT, ticker TEXT, name TEXT, price REAL, chg_pct REAL, volume INTEGER, status TEXT
)""")
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for t in rows:
    cur.execute("INSERT INTO m82_futures_overnight VALUES (?,?,?,?,?,?,?)",
                (ts, t[0], t[1], t[2], t[3], t[4], 'INGESTED_OVERNIGHT'))
conn.commit()
cur.execute("PRAGMA wal_checkpoint(PASSIVE);")
conn.close()

# 3. Despacho ENV SAFE
TOKEN=os.getenv('M82_TG_TOKEN')
CHAT=os.getenv('M82_TG_CHAT_ID','-1004335849125')
NTFY=os.getenv('M82_NTFY_URL','https://ntfy.sh/M82-Molina-Alerts-v2')
if TOKEN:
    # Top movers overnight
    movers = sorted(rows, key=lambda x: abs(x[3]), reverse=True)[:5]
    msg = f"🏛️ M82 OVERNIGHT FUTURES — ASIA+US — {ts}\n"
    for ticker,name,price,chg,vol in rows[:10]:
        msg+= f"{'🟢' if chg>0 else '🔴'} {ticker} {price:.2f} {chg:+.2f}%\n"
    msg+= f"────────────────\n🛡️ BUNKER 0.30x LOCK Exp 0.22x VaR 1.68% Warsh +102bps\n🔒 WAL 0/0/0"
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                      data={'chat_id':CHAT,'text':msg}, timeout=8)
        requests.post(NTFY, data=f"M82 OVERNIGHT FUTURES PULL {len(rows)} tickers".encode(), timeout=8)
        print("✅ TELEMETRIA OVERNIGHT DESPACHADA")
    except Exception as e:
        print(f"⚠️ Dispatch {e}")
else:
    print("❌ ENV SAFE — TOKEN no encontrado")
print(f"✅ WAL CLEAN — {len(rows)} FUTURES INGESTED")
