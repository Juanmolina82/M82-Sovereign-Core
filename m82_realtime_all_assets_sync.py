#!/usr/bin/env python3
import os
import re
import json
import time
import sqlite3
import subprocess
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
DB_PATH = BASE_DIR / "m82_database.db"

def fetch_json(url, timeout=8):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 M82-Quantum-Node/60.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))

def get_live_ticks():
    # 1. BTC/USD en tiempo real (Binance -> Coinbase fallback)
    btc_p, btc_chg = None, 0.0
    try:
        d = fetch_json("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT")
        btc_p = float(d["lastPrice"])
        btc_chg = float(d["priceChangePercent"])
    except Exception:
        try:
            d = fetch_json("https://api.coinbase.com/v2/prices/BTC-USD/spot")
            btc_p = float(d["data"]["amount"])
        except Exception:
            btc_p = 64000.00

    # 2. Brent & WTI en tiempo real (Yahoo Finance Chart API)
    def yf_quote(sym, def_p):
        try:
            d = fetch_json(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m&range=1d")
            meta = d["chart"]["result"][0]["meta"]
            p = float(meta["regularMarketPrice"])
            prev = float(meta.get("chartPreviousClose") or p)
            chg = ((p - prev) / prev * 100.0) if prev else 0.0
            return round(p, 2), round(chg, 2)
        except Exception:
            return def_p, 0.0

    brent_p, brent_chg = yf_quote("BZ=F", 95.93)
    wti_p, wti_chg = yf_quote("CL=F", 88.85)
    # Paridad fisica Merey 16 (diferencial crudo pesado USGC/Atlantico vs Brent)
    merey_p = round(brent_p - 15.25, 2)
    return round(btc_p, 2), round(btc_chg, 2), merey_p, wti_p, wti_chg, brent_p, brent_chg

# 1. Actualizar tabla m82_live_market_quotes en SQLite WAL
con = sqlite3.connect(str(DB_PATH), timeout=60.0)
con.execute("PRAGMA journal_mode=WAL;")
con.execute("PRAGMA busy_timeout=60000;")

cols = {r[1] for r in con.execute("PRAGMA table_info(m82_live_market_quotes);")}
if "btc_price" not in cols:
    con.execute("ALTER TABLE m82_live_market_quotes ADD COLUMN btc_price REAL DEFAULT 64000.0;")
if "btc_chg_pct" not in cols:
    con.execute("ALTER TABLE m82_live_market_quotes ADD COLUMN btc_chg_pct REAL DEFAULT 0.0;")

btc_p, btc_chg, merey_p, wti_p, wti_chg, brent_p, brent_chg = get_live_ticks()
ts_now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

con.execute("""
UPDATE m82_live_market_quotes
SET btc_price = ?, btc_chg_pct = ?, merey16_price = ?, wti_price = ?, wti_chg_pct = ?, brent_price = ?, brent_chg_pct = ?, updated_at = ?
WHERE id = 1;
""", (btc_p, btc_chg, merey_p, wti_p, wti_chg, brent_p, brent_chg, ts_now))
con.commit()
con.execute("PRAGMA wal_checkpoint(PASSIVE);")
con.close()

live_banner = f"BTC: ${btc_p:,.2f} ({btc_chg:+.2f}%) | MEREY 16: ${merey_p:.2f} | WTI: ${wti_p:.2f} ({wti_chg:+.2f}%) | BRENT: ${brent_p:.2f} ({brent_chg:+.2f}%)"
print(f"[+] SQLITE LIVE QUOTES SINCRONIZADO @ {ts_now}")
print(f"    {live_banner}")

# 2. Actualizar el demonio de feed continuo para que refresque BTC + Energia cada 30s
daemon_path = BASE_DIR / "desks" / "m82_realtime_energy_feed_daemon.py"
daemon_path.parent.mkdir(parents=True, exist_ok=True)
daemon_code = '''#!/usr/bin/env python3
import time, json, sqlite3, urllib.request
from datetime import datetime, timezone

DB_PATH = "/data/data/com.termux/files/home/M82/m82_database.db"

def fetch_json(url, timeout=8):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 M82-Realtime/60.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="ignore"))

def pull_ticks():
    btc_p, btc_chg = 64000.0, 0.0
    try:
        d = fetch_json("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT")
        btc_p, btc_chg = float(d["lastPrice"]), float(d["priceChangePercent"])
    except Exception:
        try:
            d = fetch_json("https://api.coinbase.com/v2/prices/BTC-USD/spot")
            btc_p = float(d["data"]["amount"])
        except Exception:
            pass

    def yf(sym, fallback):
        try:
            d = fetch_json(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m&range=1d")
            m = d["chart"]["result"][0]["meta"]
            p = float(m["regularMarketPrice"])
            prev = float(m.get("chartPreviousClose") or p)
            return round(p, 2), round(((p - prev) / prev * 100.0) if prev else 0.0, 2)
        except Exception:
            return fallback, 0.0

    brent_p, brent_chg = yf("BZ=F", 95.93)
    wti_p, wti_chg = yf("CL=F", 88.85)
    merey_p = round(brent_p - 15.25, 2)
    return round(btc_p, 2), round(btc_chg, 2), merey_p, wti_p, wti_chg, brent_p, brent_chg

while True:
    try:
        bp, bc, mp, wp, wc, brp, brc = pull_ticks()
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        con = sqlite3.connect(DB_PATH, timeout=60.0)
        con.execute("PRAGMA journal_mode=WAL;")
        con.execute("PRAGMA busy_timeout=60000;")
        con.execute("""
        UPDATE m82_live_market_quotes
        SET btc_price=?, btc_chg_pct=?, merey16_price=?, wti_price=?, wti_chg_pct=?, brent_price=?, brent_chg_pct=?, updated_at=?
        WHERE id=1;
        """, (bp, bc, mp, wp, wc, brp, brc, ts))
        con.commit()
        con.execute("PRAGMA wal_checkpoint(PASSIVE);")
        con.close()
    except Exception:
        pass
    time.sleep(30)
'''
daemon_path.write_text(daemon_code, encoding="utf-8")
daemon_path.chmod(0o755)
subprocess.run(["pkill", "-f", "m82_realtime_energy_feed_daemon.py"], stderr=subprocess.DEVNULL)
lf_d = open(BASE_DIR / "logs" / "realtime_feed.log", "a")
p_d = subprocess.Popen(["nohup", "python3", "-u", str(daemon_path)], stdout=lf_d, stderr=subprocess.STDOUT, start_new_session=True)
print(f"[+] DEMONIO MULTI-ACTIVO REINICIADO (BTC + ENERGIA cada 30s) | PID={p_d.pid}")

# 3. Inyectar lector cero-cache en todos los emisores de Telegram / HUD
LIVE_FN = '''
def _m82_live_banner():
    try:
        import sqlite3 as _s
        _c = _s.connect("file:/data/data/com.termux/files/home/M82/m82_database.db?mode=ro", uri=True, timeout=15.0)
        _r = _c.execute("SELECT btc_price, btc_chg_pct, merey16_price, wti_price, wti_chg_pct, brent_price FROM m82_live_market_quotes WHERE id=1").fetchone()
        _c.close()
        if _r and _r[0]:
            return f"BTC: ${_r[0]:,.0f} ({_r[1]:+.2f}%) | MEREY 16: ${_r[2]:.2f} | WTI: ${_r[3]:.2f} | BRENT: ${_r[5]:.2f}"
    except Exception:
        pass
    return "BTC: LIVE | MEREY 16: LIVE | WTI: LIVE | BRENT: LIVE"
'''

restarted = []
for py_file in BASE_DIR.rglob("*.py"):
    if "backups" in py_file.parts or py_file.name in ("m82_realtime_all_assets_sync.py", "m82_realtime_energy_feed_daemon.py"):
        continue
    try:
        src = py_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    if "MEREY 16:" in src or "_m82_live_banner" in src:
        if "def _m82_live_banner():" in src:
            src_new = re.sub(r'def _m82_live_banner\(\):.*?return "MEREY 16: LIVE \| WTI: LIVE \| BRENT: LIVE"\n', LIVE_FN.strip() + "\n", src, flags=re.DOTALL)
        else:
            src_new = LIVE_FN + "\n" + src
        src_new = re.sub(r'f?["\']MEREY 16:[^"\']*["\']', "_m82_live_banner()", src_new)
        if src_new != src:
            py_file.write_text(src_new, encoding="utf-8")
            restarted.append(py_file)

for fpath in restarted:
    subprocess.run(["pkill", "-f", fpath.name], stderr=subprocess.DEVNULL)
    lf = open(BASE_DIR / "logs" / f"{fpath.stem}.log", "a")
    p = subprocess.Popen(["nohup", "python3", "-u", str(fpath)], stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
    print(f"[+] EMISOR REINICIADO CON CERO-CACHE REAL-TIME: {fpath.name} | PID={p.pid}")
