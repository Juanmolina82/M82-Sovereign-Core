#!/usr/bin/env python3
import os, sqlite3, json
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

class M82Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=60000;")
        cur = conn.cursor()
        if self.path == "/health":
            cur.execute("SELECT COUNT(*) FROM macro_dossier")
            dossier_cnt = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM m82_multi_stream")
            stream_cnt = cur.fetchone()[0]
            payload = {
                "status": "ONLINE",
                "node": "CHARALLAVE_L4_L5_EDGE",
                "port": 8086,
                "governance": "BUNKER_MODE_0.30x_LOCK",
                "exposure": "0.22x",
                "var_daily": "1.68%",
                "warsh_spread_bps": 102.0,
                "macro_dossier_records": dossier_cnt,
                "multi_stream_events": stream_cnt
            }
        else:
            cur.execute("SELECT id, daemon_source, alpha_score, asset_impact, status, headline FROM m82_multi_stream ORDER BY id DESC LIMIT 5")
            rows = [{"id": r[0], "source": r[1], "alpha": r[2], "asset": r[3], "status": r[4], "headline": r[5]} for r in cur.fetchall()]
            payload = {"latest_stream": rows}
        conn.close()
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8086), M82Handler).serve_forever()
