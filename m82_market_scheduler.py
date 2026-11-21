#!/usr/bin/env python3
import time, os
from datetime import datetime
import pytz

BASE_DIR = os.path.expanduser("~/M82")
LOG_PATH = os.path.join(BASE_DIR, "lite_runner.log")

def get_current_session(vet_hour):
    if 9 <= vet_hour < 11:
        return "OVERLAP_EU_US", 15
    elif 9 <= vet_hour < 16:
        return "WALL_STREET_US", 30
    elif 3 <= vet_hour < 11:
        return "EUROPE_LONDON", 30
    elif vet_hour >= 18 or vet_hour < 2:
        return "ASIA_PACIFIC", 45
    else:
        return "OFF_PEAK_MONITOR", 60

def run_scheduler():
    tz_vet = pytz.timezone('America/Caracas')
    current_session = None
    
    while True:
        now_vet = datetime.now(tz_vet)
        session_name, poll_interval = get_current_session(now_vet.hour)

        if session_name != current_session:
            current_session = session_name
            msg = f"[{now_vet.strftime('%Y-%m-%d %H:%M:%S')} VET] 🌐 MERCADO ACTIVO: {session_name} | Polling: {poll_interval}s\n"
            with open(LOG_PATH, "a") as f:
                f.write(msg)

        time.sleep(poll_interval)

if __name__ == "__main__":
    run_scheduler()
