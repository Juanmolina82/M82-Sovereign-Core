import sqlite3

DB_PATH = "/data/data/com.termux/files/home/M82/m82_database.db"

def verify_rules():
    conn = sqlite3.connect(DB_PATH, timeout=60)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, daemon_source, alpha_score, headline FROM m82_multi_stream WHERE status='PENDING'")
    pending_rows = cursor.fetchall()
    
    for row in pending_rows:
        rec_id, src, score, headline = row
        if src == "FAJA_CRUDE_DESK" and score >= 0.96:
            # Regla de Gobernanza FAJA
            if "SPR" not in headline and "shadow fleet" not in headline:
                print(f"[M82 VERIFIER] ID {rec_id} FAJA_CRUDE held in PENDING — Lack of SPR/Shadow Fleet trigger.")
                continue
            
            cursor.execute("UPDATE m82_multi_stream SET status='VERIFIED' WHERE id=?", (rec_id,))
            print(f"[M82 VERIFIER] ID {rec_id} VERIFIED via Rule Pass.")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    verify_rules()
