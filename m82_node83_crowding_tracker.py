#!/usr/bin/env python3
import os, sys, time, sqlite3, requests, xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS m82_multi_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_source TEXT,
            headline TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [NODE83-CROWDING-TRACKER] {msg}", flush=True)

def inject_signal(source, headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        """, (source, headline))
        conn.commit()
        log(f"✅ [{source}] Inyectado: {headline[:65]}...")
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        log(f"❌ Error DB: {e}")

FEEDS_NODE83 = {
    "NODE83_YIELD_MONITOR": "https://news.google.com/rss/search?q=(%22Treasury+auction+39B%22+OR+%2210-year+yield+5.36%22)+when:1d&hl=en-US&gl=US&ceid=US:en",
    "NODE83_VENZ_SOVEREIGN": "https://news.google.com/rss/search?q=(%22Venezuela+bonds+default%22+OR+%22Centerview+restructuring%22)+when:1d&hl=en-US&gl=US&ceid=US:en",
    "NODE83_CROWDING_TECH": "https://news.google.com/rss/search?q=(%22SpaceX+bond+offering%22+OR+%22hyperscaler+debt+capex%22)+when:1d&hl=en-US&gl=US&ceid=US:en"
}

def scan_node83():
    for source, url in FEEDS_NODE83.items():
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall('.//item')[:2]:
                    title = item.find('title').text
                    if " - " in title:
                        title = title.rsplit(" - ", 1)[0]
                    inject_signal(source, title.strip())
        except Exception as e:
            log(f"⚠️ Error escaneando {source}: {e}")

def main():
    init_db()
    log("🚀 Daemon Node 83: Post-Hike Crowding Tracker Activo.")
    inject_signal("M82_NODE83_OPEN", "NODE 83 ACTIVATED: Post-Hike Crowding | US10Y 5.36% vs Private Credit Drain & TSLA -2x Transmission")

    while True:
        scan_node83()
        time.sleep(120)

if __name__ == "__main__":
    main()
