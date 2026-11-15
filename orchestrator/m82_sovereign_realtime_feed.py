#!/usr/bin/env python3
import os, time, json, hashlib, sqlite3, subprocess, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_orchestrator_wal.db")
SEEN_FILE = os.path.expanduser("~/M82/.seen_breaking_hashes.json")

SYMBOLS = {
    "CL=F": "WTI CRUDE",
    "BZ=F": "BRENT CRUDE",
    "RB=F": "RBOB GAS",
    "HO=F": "HEATING OIL",
    "^TNX": "US 10Y",
    "DX-Y.NYB": "DXY",
    "NVDA": "NVDA",
    "BTC-USD": "BTC-USD"
}

RSS_FEEDS = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=CL=F,BZ=F,NVDA,SPY,QQQ&region=US&lang=en-US",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://www.cnbc.com/id/100727362/device/rss/rss.html",
    "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
    "https://feeds.bbci.co.uk/news/business/rss.xml"
]

def load_seen():
    try:
        return set(json.load(open(SEEN_FILE)))
    except Exception:
        return set()

def save_seen(seen):
    try:
        json.dump(list(seen)[-500:], open(SEEN_FILE, "w"))
    except Exception:
        pass

def push_android_alert(title, body, nid):
    try:
        subprocess.Popen([
            "termux-notification",
            "--id", str(nid),
            "--group", "M82_BREAKING_WIRE",
            "--title", f"🔴 M82 BREAKING • {title}",
            "--content", body,
            "--priority", "max",
            "--vibrate", "120,60,120",
            "--action", "termux-open-url http://127.0.0.1:8282"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def fetch_quotes():
    out = []
    for sym, label in SYMBOLS.items():
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m&range=1d"
            req = urllib.request.Request(url, headers={"User-Agent": "M82-Sovereign-Engine/4.2"})
            with urllib.request.urlopen(req, timeout=6) as r:
                meta = json.loads(r.read().decode("utf-8"))["chart"]["result"][0]["meta"]
                px = float(meta.get("regularMarketPrice"))
                prev = float(meta.get("chartPreviousClose") or px)
                chg = ((px - prev) / prev * 100.0) if prev else 0.0
                out.append((sym, label, round(px, 2), round(chg, 2)))
        except Exception:
            pass
    return out

def fetch_headlines():
    items = []
    for feed in RSS_FEEDS:
        try:
            req = urllib.request.Request(feed, headers={"User-Agent": "M82-Sovereign-Engine/4.2"})
            with urllib.request.urlopen(req, timeout=6) as r:
                root = ET.fromstring(r.read())
                for item in root.findall(".//item")[:6]:
                    t = (item.findtext("title") or "").strip()
                    if t:
                        items.append(t)
        except Exception:
            pass
    return items

def sanitize_brand(text):
    for bad in ("Reuters", "REUTERS", "LSEG", "Refinitiv", "BBC", "CNBC", "Yahoo"):
        text = text.replace(bad, "M82 Wire")
    return text

def is_macro_relevant(t):
    low = t.lower()
    noise = ("beauty", "advent calendar", "fashion", "celebrity", "recipe", "horoscope", "kardashian")
    return not any(n in low for n in noise)

def sync_cycle():
    seen = load_seen()
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    cur = conn.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    quotes = fetch_quotes()
    headlines = fetch_headlines()
    new_alerts = 0

    target_tbl = next((t for t in tables if any(k in t.lower() for k in ("news", "wire", "event", "feed", "dispatch", "log"))), None)
    cols = [c[1] for c in cur.execute(f"PRAGMA table_info({target_tbl})").fetchall()] if target_tbl else []

    # 1. Procesar titulares en vivo y disparar Push inmediato en pantalla de bloqueo
    for raw_hl in headlines:
        h_hash = hashlib.sha256(raw_hl.encode("utf-8")).hexdigest()[:16]
        if h_hash not in seen:
            seen.add(h_hash)
            clean_hl = sanitize_brand(raw_hl)
            if len(cols) >= 3:
                cur.execute(f"INSERT INTO {target_tbl} ({cols[1]}, {cols[2]}) VALUES (?, ?)", (now_iso, f"[M82 BREAKING WIRE] {clean_hl}"))
            push_android_alert("MACRO & GEOPOLITICAL FLASH", clean_hl, int(h_hash[:6], 16) % 90000 + 1000)
            new_alerts += 1

    # 2. Actualizar telemetria cuantitativa y alertar variaciones bruscas (>= 1.5%)
    if len(cols) >= 3:
        for q_sym, q_lbl, q_px, q_chg in quotes:
            cur.execute(f"INSERT INTO {target_tbl} ({cols[1]}, {cols[2]}) VALUES (?, ?)", (now_iso, f"[M82 QUANTUM TELEMETRY] {q_lbl} ({q_sym}): {q_px} ({q_chg:+.2f}%) | BUNKER 0.30x LOCK"))
            if abs(q_chg) >= 1.5:
                m_hash = hashlib.sha256(f"{q_sym}:{round(q_chg,1)}".encode()).hexdigest()[:16]
                if m_hash not in seen:
                    seen.add(m_hash)
                    push_android_alert(f"MARKET MOVE • {q_lbl}", f"{q_lbl} ({q_sym}) {q_chg:+.2f}% @ {q_px}", int(m_hash[:6], 16) % 90000 + 1000)

    conn.commit()
    conn.close()
    save_seen(seen)
    print(f"[{now_iso}] Ciclo 15s OK | Nuevas Alertas Push: {new_alerts} | Activos: {len(quotes)}")

if __name__ == "__main__":
    while True:
        try:
            sync_cycle()
        except Exception as e:
            print(f"[M82 PUSH WARN] {e}")
        time.sleep(15)
