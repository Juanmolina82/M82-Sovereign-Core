import sqlite3, time, os
from datetime import datetime

DB = os.path.expanduser("~/M82/m82_database.db")
TRIGGER = 98.0

while True:
    try:
        conn = sqlite3.connect(DB, timeout=15.0)
        row = conn.execute("SELECT brent, headline FROM m82_multi_stream WHERE brent IS NOT NULL ORDER BY id DESC LIMIT 1").fetchone()
        conn.close()
        if row:
            brent = float(row[0])
            if brent < TRIGGER:
                msg = f"🚨 M82 BREAKOUT: BRENT ${brent:.2f} <${TRIGGER} - MIDTERMS COVERED - Eval unlock 0.30x -> 0.40x"
                print(f"[{datetime.now()}] {msg}")
                os.system(f'termux-notification --title "M82 BRENT ALERT" --content "{msg}" --priority high 2>/dev/null')
                conn = sqlite3.connect(DB, timeout=15.0)
                conn.execute(
                    "INSERT INTO m82_multi_stream (daemon_source, headline, brent, bunker, status, created_at) VALUES (?,?,?,?,?,?)",
                    ("M82_ALERT_DAEMON", msg, brent, 0.40, "ALERT_TRIGGERED", datetime.now().isoformat())
                )
                conn.commit()
                conn.close()
    except Exception as e:
        print(f"[ALERT ERR]: {e}")
    time.sleep(60)
