#!/usr/bin/env python3
import os, json, sqlite3, hashlib

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

class ResilienceLayer:
    def log_forensic_event(self, event_type, payload_str):
        data_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        conn = sqlite3.connect(DB_PATH, timeout=60.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO m82_forensic_audit (event_type, data_hash, payload)
            VALUES (?, ?, ?)
        """, (event_type, data_hash, payload_str))
        conn.commit()
        conn.close()
        return data_hash

if __name__ == "__main__":
    resilience = ResilienceLayer()
    h = resilience.log_forensic_event("AUDIT_CHECK", "Resiliencia activa.")
    print(f"🛡️ [NIVEL 5] Audit Hash registrado.")
