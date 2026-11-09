#!/usr/bin/env python3
import os, sys, time, sqlite3, requests
import xml.etree.ElementTree as ET

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def insert_headline(headline):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        c = conn.cursor()
        c.execute('''
            INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', CURRENT_TIMESTAMP)
        ''', ('FIRM_RANKING', headline))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        pass
    except Exception:
        pass

def scan():
    url = f"https://news.google.com/rss/search?q=Asset+Manager+AUM+Ranking&hl=en-US&gl=US&ceid=US:en"
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            for item in root.findall('.//item')[:2]:
                title = item.find('title').text
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0]
                insert_headline(title.strip())
    except Exception:
        pass

def main():
    while True:
        scan()
        time.sleep(180)

if __name__ == "__main__":
    main()
