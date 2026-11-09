#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

feeds = [
    {"source": "VE_DESK_EXILE", "headline": "VENEZUELA: Jefa de comunicaciones de Maria Corina Machado regresa tras 1.5 años de exilio"},
    {"source": "VE_DESK_MOBILIZE", "headline": "VENEZUELA MOBILIZATION: Supporters of Maria Corina Machado mobilize demanding safe return and elections"},
    {"source": "VE_DESK_DIPLOMACY", "headline": "VENEZUELA GEOPOLITICS: International pressure grows for transparent electoral roadmap in Venezuela"}
]

def run():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    
    count = 0
    for item in feeds:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', ?)
        """, (item["source"], item["headline"], now))
        if c.rowcount > 0: count += 1
        
    conn.commit()
    conn.close()
    print(f"🇻🇪 [DAEMON VENEZUELA]: Inyectadas {count} nuevas señales.")

if __name__ == "__main__":
    run()
