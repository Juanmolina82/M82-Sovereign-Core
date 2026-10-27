#!/usr/bin/env python3
from m82_db import execute_query

def update_checklist_counter(brent=106.14, dubai_premium=13.14, diesel_shock=1):
    is_red_day = 1 if (brent >= 100.0 and (dubai_premium >= 12.0 or diesel_shock == 1)) else 0
    
    res = execute_query("SELECT consecutive_red_days FROM m82_mcm_checklist ORDER BY id DESC LIMIT 1;", fetch=True)
    prev_days = res[0][0] if (res and len(res) > 0) else 0
    current_consecutive = (prev_days + 1) if is_red_day else 0
    
    try:
        execute_query("""
            INSERT INTO m82_mcm_checklist 
            (brent_price, dubai_squeeze, diesel_shock_active, red_day_flag, consecutive_red_days)
            VALUES (?, ?, ?, ?, ?);
        """, (brent, dubai_premium, diesel_shock, is_red_day, current_consecutive))
    except Exception:
        execute_query("""
            UPDATE m82_mcm_checklist 
            SET brent_price = ?, dubai_squeeze = ?, diesel_shock_active = ?, 
                red_day_flag = ?, consecutive_red_days = ?
            WHERE date = DATE('now');
        """, (brent, dubai_premium, diesel_shock, is_red_day, current_consecutive))

    print(f"📊 [M82 CHECKLIST STATUS] Días continuos en ROJO: {current_consecutive}/90 | Brent: ${brent}")

    if current_consecutive >= 90:
        headline = f"🚨 M82 MACRO ALERT: 90 CONTINUOUS RED DAYS REACHED ({current_consecutive}/90) | MCM Energy Window Unlocked"
        execute_query("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status)
            VALUES ('M82_MCM_CHECKLIST', ?, 'PENDING');
        """, (headline,))

if __name__ == "__main__":
    update_checklist_counter()
