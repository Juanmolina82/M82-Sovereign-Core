#!/usr/bin/env python3
import sqlite3, os, json, time
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
OUTPUT_SIGNAL_PATH = os.path.expanduser("~/M82/m82_fused_signal.json")

class FusionEngine:
    def fetch_pending_signals(self):
        conn = sqlite3.connect(DB_PATH, timeout=60.0)
        cursor = conn.cursor()
        cursor.execute("SELECT id, daemon_source, headline, timestamp FROM m82_multi_stream WHERE status = 'PENDING' LIMIT 1")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def process_fusion(self):
        pending = self.fetch_pending_signals()
        if not pending:
            return None

        row = pending[0]
        fusion_payload = {
            "timestamp_utc": datetime.utcnow().isoformat(),
            "source": row[1],
            "unified_summary": row[2],
            "row_id": row[0]
        }

        with open(OUTPUT_SIGNAL_PATH, "w") as f:
            json.dump(fusion_payload, f, indent=4)

        return fusion_payload

if __name__ == "__main__":
    engine = FusionEngine()
    result = engine.process_fusion()
    if result:
        print("🧠 [NIVEL 3] Fusión lista.")
