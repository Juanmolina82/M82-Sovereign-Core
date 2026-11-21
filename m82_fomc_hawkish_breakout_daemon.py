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
    print(f"[{timestamp}] [HAWKISH-BREAKOUT-DAEMON] {msg}", flush=True)

def inject_signal(source, headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        """, (source, headline))
        conn.commit()
        log(f"✅ [{source}] Señal Hawkish Inyectada: {headline[:65]}...")
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        log(f"❌ Error en DB: {e}")

FEEDS_POST_FOMC = {
    "FOMC_HAWKISH_TRANSMISSION": "https://news.google.com/rss/search?q=(%22Fed+rate+hike%22+OR+%22FOMC+minutes%22+OR+%22Treasury+yields+5.36%22)+when:1d&hl=en-US&gl=US&ceid=US:en",
    "PRIVATE_CREDIT_DRAIN": "https://news.google.com/rss/search?q=(%22SpaceX+bond%22+OR+%22private+credit+yields%22+OR+%22crowding+out%22)+when:1d&hl=en-US&gl=US&ceid=US:en"
}

def scan_post_fomc():
    for source, url in FEEDS_POST_FOMC.items():
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall('.//item')[:3]:
                    title = item.find('title').text
                    if " - " in title:
                        title = title.rsplit(" - ", 1)[0]
                    inject_signal(source, title.strip())
        except Exception as e:
            log(f"⚠️ Error en scan: {e}")

def main():
    init_db()
    log("🚀 Daemon de Transmisión Hawkish Post-FOMC Activo.")
    catalyst_headline = "FOMC BREAKOUT: Most Officials See Another Rate Hike in 2026 | US10Y 5.36% Accelerates Private Credit Drain"
    inject_signal("FOMC_HAWKISH_BREAKOUT", catalyst_headline)

    while True:
        scan_post_fomc()
        time.sleep(120)

if __name__ == "__main__":
    main()
