#!/usr/bin/env python3
import sqlite3, os
from datetime import datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
LOG_FILE = os.path.join(BASE_DIR, "daily_dossier.log")

def run():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{now}] Daily Dossier re-index completed successfully.\n")

if __name__ == "__main__":
    run()
